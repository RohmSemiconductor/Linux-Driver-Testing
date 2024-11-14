#include <linux/module.h>
#include <linux/platform_device.h>
#include <linux/of.h>
#include <linux/sysfs.h>
#include <linux/iio/consumer.h>
#include <linux/iio/iio.h>
#include <linux/iio/types.h>
#include <linux/iio/buffer.h>
#include <linux/container_of.h>
#include <linux/kfifo.h>
#include <linux/completion.h>

struct scan {
	__le16 channels[3];
	s64 ts __aligned(8);
};

struct accel_priv {
	struct iio_cb_buffer *buffer;
	struct iio_channel *channel;
	struct scan *scan;
	int axis_bits;
	int en_cb_buffer;
	uint32_t fifo_size;
	DECLARE_KFIFO_PTR(kfifo_accel, struct scan);
	unsigned int watermark;
	struct completion kfifo_at_wm;
};

#define FIFO_SIZE	128
#define AXIS_COUNT	3
const unsigned int ms2_mult = 1000;

enum INT_TO_FRAC {
	INT_TO_FRAC_MICRO = 6,
	INT_TO_FRAC_NANO = 9
};

enum AXIS_INFO {
	AXIS_X = 4,
	AXIS_Y = 2,
	AXIS_Z = 1
};

static void pscale_split_to_ints(int val, unsigned int mult, int *value1,
				 int *value2)
{
	*value1 = val/(int)mult;
	*value2 = val%(int)mult;
	if (*value2 < 0)
		*value2 = *value2 * -1;
}

static int char_to_frac(char f[], enum INT_TO_FRAC FRAC)
{
	int retval;
	int res;

	while (strlen(f) < FRAC) {
		strcat(f,"0");
	}

	retval = kstrtoint(f,10,&res);

	if (retval != 0) {
		pr_err("char_to_frac error: %d\n", retval);
		return retval;
	}
	pr_info("res: %d\n", res);
	return res;
}

static ssize_t en_cb_buffer_show (struct device *dev,
				  struct device_attribute *attr,
				  char *b)
{
	int rval;
	struct accel_priv *accel_priv = dev_get_drvdata(dev);

	rval = sprintf(b, "%d\n", accel_priv->en_cb_buffer);

	return rval;
}

static ssize_t en_cb_buffer_store (struct device *dev,
				   struct device_attribute *attr,
				   const char *b, size_t c)
{
	int rval;
	int endis_buffer;
	struct accel_priv *accel_priv = dev_get_drvdata(dev);

	rval = sscanf(b, "%d",&endis_buffer);

	if (endis_buffer == 0) {
		iio_channel_stop_all_cb(accel_priv->buffer);
		pr_info("stop cb buffer\n");
	}
	else if (endis_buffer == 1) {
		iio_channel_stop_all_cb(accel_priv->buffer);
		kfifo_reset_out(&accel_priv->kfifo_accel);
		iio_channel_start_all_cb(accel_priv->buffer);
		pr_info("start cb buffer\n");
	}

	accel_priv->en_cb_buffer = endis_buffer;

	rval = c;
	return rval;
}

DEVICE_ATTR_RW(en_cb_buffer);

static ssize_t scale_available_show (struct device *dev,
				     struct device_attribute *attr,
				     char *b)
{
	int rval;
	struct accel_priv *accel_priv = dev_get_drvdata(dev);
	int type;
	int length;
	const int *list_vals;
	const int **vals = &list_vals;
	char freq_avail[100];
	char fval[15];

	rval = iio_read_avail_channel_attribute(accel_priv->channel, vals,
						&type, &length,
						IIO_CHAN_INFO_SCALE);

	if (rval < 0) {
		pr_err("Problems reading available scales! Errno: %d", rval);
		return rval;
	}

	for (int x=0; x < length; x=x+2) {
		sprintf(fval, "%d.", vals[0][x]);
		strcat(freq_avail,fval);
		sprintf(fval, "%09d ", vals[0][x+1]);
		strcat(freq_avail, fval);
	}
	rval = sprintf(b,"%s\n", freq_avail);
	return rval;
}

DEVICE_ATTR_RO(scale_available);

static ssize_t sampling_frequency_available_show (struct device *dev,
						  struct device_attribute *attr,
						  char *b)
{
	int rval;
	struct accel_priv *accel_priv = dev_get_drvdata(dev);
	int type;
	int length;
	const int *list_vals;
	const int **vals = &list_vals;
	char freq_avail[100];
	char fval[15];

	rval = iio_read_avail_channel_attribute(accel_priv->channel, vals,
						&type, &length,
						IIO_CHAN_INFO_SAMP_FREQ);

	if (rval < 0) {
		pr_err("Problems reading available sampling frequencies! "
		       "Errno: %d", rval);

		return rval;
	}

	for (int x=0; x < length; x=x+2) {
		sprintf(fval, "%d.", vals[0][x]);
		strcat(freq_avail,fval);
		sprintf(fval, "%d ", vals[0][x+1]);
		strcat(freq_avail, fval);
	}
	rval = sprintf(b,"%s\n", freq_avail);
	return rval;
}
DEVICE_ATTR_RO(sampling_frequency_available);

static ssize_t watermark_show (struct device *dev,
			       struct device_attribute *attr, char *b)
{
	int rval;
	struct accel_priv *accel_priv = dev_get_drvdata(dev);

	rval = sprintf(b, "%d\n", accel_priv->watermark);
	pr_info("write only\n");

	return rval;
}

static ssize_t watermark_store (struct device *dev,
				struct device_attribute *attr,
				const char *b, size_t c)
{
	int rval;
	unsigned int watermark;
	struct accel_priv *accel_priv = dev_get_drvdata(dev);

	iio_channel_stop_all_cb(accel_priv->buffer);
	pr_info("iio_channel_stop_all_cb called!\n");

	rval = sscanf(b, "%d", &watermark);

	rval = iio_channel_cb_set_buffer_watermark(accel_priv->buffer,
						   watermark);

	pr_info("iio_channel_cb_set_buffer_watermark called!\n");

	pr_info("watermark_store rval: %d\n",rval);

	if (rval != 0)
		pr_err("watermark error: %d\n", rval);
	else if (watermark > accel_priv->fifo_size)
		accel_priv->watermark = accel_priv->fifo_size;
	else
		accel_priv->watermark = watermark;

	rval = iio_channel_start_all_cb(accel_priv->buffer);
	pr_info("iio_channel_start_all_cb called!\n");

	if (rval != 0)
		pr_err("iio_channel_start_all_cb: %d\n", rval);

	iio_channel_stop_all_cb(accel_priv->buffer);

	accel_priv->en_cb_buffer = 0;
	pr_info("iio_channel_stop_all_cb called!\n");
	rval = c;
	return rval;
}

DEVICE_ATTR_RW(watermark);

static ssize_t sampling_frequency_show (struct device *dev,
					struct device_attribute *attr, char *b)
{
	int rval;
	struct accel_priv *accel_priv = dev_get_drvdata(dev);
	int val;
	int val2;

	rval = iio_read_channel_attribute(accel_priv->channel, &val, &val2,
					  IIO_CHAN_INFO_SAMP_FREQ);
	if (val < 0)
		pr_err("iio_read_channel_attribute errno %d\n", rval);

	rval = sprintf(b, "%d.%06d\n", val, val2);

	return rval;
}

static ssize_t sampling_frequency_store (struct device *dev,
					 struct device_attribute *attr,
					 const char *b, size_t c)
{
	struct accel_priv *accel_priv = dev_get_drvdata(dev);
	int rval;
	int val;
	int val2;
	char val2_buffer[7];

	rval = sscanf(b, "%d.%6s", &val, val2_buffer);

	if (rval < 2) {
		val2 = 0;
	}
	else {
		val2 = char_to_frac(val2_buffer, INT_TO_FRAC_MICRO);

		if (val2 < 0 ) {
			pr_err("Dont put stuff where it does not belong! "
			       "Error: %d\n", val2);

			return val2;
		}
	}

	rval = iio_write_channel_attribute(accel_priv->channel, val, val2,
					   IIO_CHAN_INFO_SAMP_FREQ);

	if (rval < 0)
	{
		pr_err("SAMP_FREQ: iio_write_channel_attribute "
		       "errno %d\n", rval);

		return rval;
	}

	pr_info("Sampling frequency set to: %d.%d\n", val, val2);
	rval = c;
	return rval;
}

DEVICE_ATTR_RW(sampling_frequency);

static ssize_t scale_show (struct device *dev, struct device_attribute *attr,
			   char *b)
{
	int rval;
	int val;
	int val2;
	struct accel_priv *accel_priv = dev_get_drvdata(dev);

	rval = iio_read_channel_attribute(accel_priv->channel, &val, &val2,
					  IIO_CHAN_INFO_SCALE);
	if (rval < 0)
		pr_err("SCALE: iio_read_channel_attribute errno %d\n", rval);
	rval = sprintf(b, "%d.%09d\n", val, val2);

	return rval;
}

static ssize_t scale_store (struct device *dev, struct device_attribute *attr,
			    const char *b, size_t c)
{
	int rval;
	int val;
	int val2;
	char val2_buffer[10];
	struct accel_priv *accel_priv = dev_get_drvdata(dev);

	rval = sscanf(b, "%d.%9s", &val, val2_buffer);

	val2 = char_to_frac(val2_buffer, INT_TO_FRAC_NANO);
	if (val2 < 0 ) {
		pr_err("Dont put stuff where it does not belong! "
		       "Error: %d\n", val2);

		return val2;
	}

	rval = iio_write_channel_attribute(accel_priv->channel, val, val2,
					   IIO_CHAN_INFO_SCALE);

	if (rval < 0)
	{
		pr_err("iio_write_channel_attribute errno %d\n", rval);
		return rval;
	}

	pr_info("Scale written: %d.%d\n", val, val2);

	rval = c;
	return rval;
}

DEVICE_ATTR_RW(scale);

static ssize_t set_enabled_buffer_store (struct device *dev,
					 struct device_attribute *attr,
					 const char *b, size_t c)
{
	int rval;
	char channels[4];
	int channels_given = 0;
	int channels_stored = 0;
	char extracted_char;
	struct accel_priv *accel_priv = dev_get_drvdata(dev);

	accel_priv->axis_bits = 0;

	sscanf(b, "%s", channels);
	channels_given = strlen(channels);

	while (channels_given > channels_stored) {
		extracted_char = channels[channels_stored];
		if (strncmp(&extracted_char, "x", 1) == 0)
			accel_priv->axis_bits = accel_priv->axis_bits + AXIS_X;
		else if (strncmp(&extracted_char, "y", 1) == 0)
			accel_priv->axis_bits = accel_priv->axis_bits + AXIS_Y;
		else if (strncmp(&extracted_char, "z", 1) == 0)
			accel_priv->axis_bits = accel_priv->axis_bits + AXIS_Z;
		pr_info("extracted_char: %c\n", extracted_char);
		channels_stored++;
	}

	pr_info("axis_bits: %d\n", accel_priv->axis_bits);

	rval = c;
	return rval;
}

DEVICE_ATTR_WO(set_enabled_buffer);

static ssize_t show_enabled_buffer_show (struct device *dev,
					 struct device_attribute *attr, char *b)
{
	int rval = 0;
	int kfifo_rval;
	struct accel_priv *accel_priv = dev_get_drvdata(dev);
	struct scan buf_out;

	if (accel_priv->axis_bits == 0) {
		rval = sprintf(b, "No channels assigned to read!\n");
		return rval;
	}
	else if (accel_priv->en_cb_buffer == 0) {
		rval = sprintf(b, "Enable buffer first!\n");
		return rval;
	}

	wait_for_completion(&accel_priv->kfifo_at_wm);

	for (int x = 0; x < accel_priv->watermark; x++) {
		kfifo_rval = kfifo_out(&accel_priv->kfifo_accel,&buf_out, 1);

		if (accel_priv->axis_bits & AXIS_X)
			rval += sprintf(b + rval, "%d ",
				(int16_t)buf_out.channels[0]);

		if (accel_priv->axis_bits & AXIS_Y)
			rval += sprintf(b + rval, "%d ",
				(int16_t)buf_out.channels[1]);

		if (accel_priv->axis_bits & AXIS_Z)
			rval += sprintf(b + rval, "%d ",
				(int16_t)buf_out.channels[2]);

	rval += sprintf(b + rval, "\n");
	}

	reinit_completion(&accel_priv->kfifo_at_wm);

	return rval;
}

DEVICE_ATTR_RO(show_enabled_buffer);

static ssize_t x_buffer_show (struct device *dev, struct device_attribute *attr,
			      char *b)
{
	int rval = 0;
	int kfifo_rval;
	struct scan buf_out;
	struct accel_priv *accel_priv = dev_get_drvdata(dev);

	if (accel_priv->en_cb_buffer == 0) {
		rval = sprintf(b, "Enable buffer first!\n");
		return rval;
	}

	wait_for_completion(&accel_priv->kfifo_at_wm);

	for (int x = 0; x < accel_priv->watermark; x++) {
		kfifo_rval = kfifo_out(&accel_priv->kfifo_accel,&buf_out, 1);
		rval += sprintf(b + rval, "%d\n", buf_out.channels[0]);
	}

	reinit_completion(&accel_priv->kfifo_at_wm);

	return rval;
}

DEVICE_ATTR_RO(x_buffer);

static ssize_t y_buffer_show (struct device *dev, struct device_attribute *attr,
			      char *b)
{
	int rval = 0;
	int kfifo_rval;
	struct scan buf_out;
	struct accel_priv *accel_priv = dev_get_drvdata(dev);

	if (accel_priv->en_cb_buffer == 0) {
		rval = sprintf(b, "Enable buffer first!\n");
		return rval;
	}

	wait_for_completion(&accel_priv->kfifo_at_wm);

	for (int x = 0; x < accel_priv->watermark; x++) {
		kfifo_rval = kfifo_out(&accel_priv->kfifo_accel,&buf_out, 1);
		rval += sprintf(b + rval, "%d\n", buf_out.channels[1]);
	}

	reinit_completion(&accel_priv->kfifo_at_wm);

	return rval;
}

DEVICE_ATTR_RO(y_buffer);

static ssize_t z_buffer_show (struct device *dev, struct device_attribute *attr,
			      char *b)
{
	int rval = 0;
	int kfifo_rval;
	struct scan buf_out;
	struct accel_priv *accel_priv = dev_get_drvdata(dev);

	if (accel_priv->en_cb_buffer == 0) {
		rval = sprintf(b, "Enable buffer first!\n");
		return rval;
	}

	wait_for_completion(&accel_priv->kfifo_at_wm);

	for (int x = 0; x < accel_priv->watermark; x++) {
		kfifo_rval = kfifo_out(&accel_priv->kfifo_accel,&buf_out, 1);
		rval += sprintf(b + rval, "%d\n", buf_out.channels[2]);
	}

	reinit_completion(&accel_priv->kfifo_at_wm);

	return rval;
}

DEVICE_ATTR_RO(z_buffer);

static ssize_t x_raw_show (struct device *dev, struct device_attribute *attr,
			   char *b)
{
	int rval;
	int val;
	struct accel_priv *accel_priv = dev_get_drvdata(dev);

	iio_channel_stop_all_cb(accel_priv->buffer);
	pr_info("iio_channel_stop_all_cb called!\n");

	rval = iio_read_channel_raw(&accel_priv->channel[0], &val );

	if (rval < 0)
		pr_err("iio_read_channel_raw errno: %d\n", rval);

	rval = sprintf(b,"%d\n",val);

	return rval;
}

DEVICE_ATTR_RO(x_raw);

static ssize_t y_raw_show (struct device *dev, struct device_attribute *attr,
			   char *b)
{
	int rval;
	struct accel_priv *accel_priv = dev_get_drvdata(dev);
	int val;

	iio_channel_stop_all_cb(accel_priv->buffer);
	pr_info("iio_channel_stop_all_cb called!\n");

	rval = iio_read_channel_raw(&accel_priv->channel[1], &val );

	if (rval < 0)
		pr_err("iio_read_channel_raw errno: %d\n", rval);

	rval = sprintf(b,"%d\n",val);

	return rval;
}

DEVICE_ATTR_RO(y_raw);

static ssize_t z_raw_show (struct device *dev, struct device_attribute *attr,
		           char *b)
{
	int rval;
	struct accel_priv *accel_priv = dev_get_drvdata(dev);
	int val;

	iio_channel_stop_all_cb(accel_priv->buffer);
	pr_info("iio_channel_stop_all_cb called!\n");

	rval = iio_read_channel_raw(&accel_priv->channel[2], &val );

	if (rval < 0)
		pr_err("iio_read_channel_raw errno: %d\n", rval);

	rval = sprintf(b,"%d\n",val);

	return rval;
}

DEVICE_ATTR_RO(z_raw);

static ssize_t x_ms2_show (struct device *dev, struct device_attribute *attr,
			   char *b)
{
	int rval;
	struct accel_priv *accel_priv = dev_get_drvdata(dev);
	int val;
	int value1;
	int value2;

	rval = iio_read_channel_processed_scale(&accel_priv->channel[0], &val,
						ms2_mult);

	if (rval < 0)
		pr_err("iio_read_channel_raw errno: %d\n", val);

	pscale_split_to_ints(val, ms2_mult, &value1, &value2);

	rval = sprintf(b,"%d.%d\n",value1, value2);

	return rval;
}

DEVICE_ATTR_RO(x_ms2);

static ssize_t y_ms2_show (struct device *dev, struct device_attribute *attr,
			   char *b)
{
	int rval;
	struct accel_priv *accel_priv = dev_get_drvdata(dev);
	int val;
	int value1;
	int value2;

	rval = iio_read_channel_processed_scale(&accel_priv->channel[1], &val,
						ms2_mult);

	if (rval < 0)
		pr_err("iio_read_channel_raw errno: %d\n", val);

	pscale_split_to_ints(val, ms2_mult, &value1, &value2);

	rval = sprintf(b,"%d.%d\n",value1, value2);

	return rval;
}

DEVICE_ATTR_RO(y_ms2);

static ssize_t z_ms2_show (struct device *dev, struct device_attribute *attr,
			   char *b)
{
	int rval;
	struct accel_priv *accel_priv = dev_get_drvdata(dev);
	int val;
	int value1;
	int value2;

	rval = iio_read_channel_processed_scale(&accel_priv->channel[2], &val,
						ms2_mult);

	if (rval < 0)
		pr_err("iio_read_channel_raw errno: %d\n", val);

	pscale_split_to_ints(val, ms2_mult, &value1, &value2);

	rval = sprintf(b,"%d.%d\n",value1, value2);

	return rval;
}

DEVICE_ATTR_RO(z_ms2);

/*
static ssize_t timestamp_show (struct kobject *ko, struct kobj_attribute *a, char *b)
{
	int rval;
//	struct iio_channel *chan = g_chan;

	rval = iio_read_channel_raw(&chan[3], &val);

	if (rval < 0)
		pr_err("iio_read_channel_raw errno: %d\n", cb_priv.scan->ts);
//	rval = sprintf(b,"%lld\n",cb_priv.scan->ts);
	rval = sprintf(b,"Dont use this for now\n");

	return rval;
}
static struct kobj_attribute timestamp = __ATTR_RO(timestamp);
*/

static struct attribute *generic_accel_test_attrs[] = {
	&dev_attr_set_enabled_buffer.attr,
	&dev_attr_show_enabled_buffer.attr,
	&dev_attr_en_cb_buffer.attr,
	&dev_attr_scale_available.attr,
	&dev_attr_sampling_frequency_available.attr,
	&dev_attr_watermark.attr,
	&dev_attr_sampling_frequency.attr,
	&dev_attr_scale.attr,
	&dev_attr_x_buffer.attr,
	&dev_attr_y_buffer.attr,
	&dev_attr_z_buffer.attr,
	&dev_attr_x_raw.attr,
	&dev_attr_y_raw.attr,
	&dev_attr_z_raw.attr,
	&dev_attr_x_ms2.attr,
	&dev_attr_y_ms2.attr,
	&dev_attr_z_ms2.attr,
//	&timestamp.attr,
	NULL
};


static const struct attribute_group generic_accel_test_group[] = {
	{
		.name = "iio_channels",
		.attrs = &generic_accel_test_attrs[0],
	}
};

static const struct attribute_group *generic_accel_test_attr_groups[] = {
	generic_accel_test_group,
	NULL
};

static int cb(const void *data, void *private)
{
	pr_info("callback kutsuttu\n");
	struct accel_priv *accel_priv;
	accel_priv = (struct accel_priv*)private;

	struct scan *buf_data;
	buf_data = (struct scan*)data;

	struct scan *cp_buf_data;
	cp_buf_data = kmemdup(buf_data, sizeof(*cp_buf_data), GFP_KERNEL);

	for(int x=0; x<AXIS_COUNT; x++) {
	       cp_buf_data->channels[x] = le16_to_cpu(cp_buf_data->channels[x]);
	       pr_info("x: %d\n",x);
	}

	kfifo_in(&accel_priv->kfifo_accel, cp_buf_data,1);
	pr_info("%d\n", cp_buf_data->channels[0]);

	if (kfifo_len(&accel_priv->kfifo_accel) >= accel_priv->watermark)
		complete(&accel_priv->kfifo_at_wm);

	return 0;
}

static int generic_accel_test_probe(struct platform_device *pdev)
{
	dev_info(&pdev->dev, "Ver 040\n");

	int rval = 0;
	struct accel_priv *accel_priv;

	accel_priv = devm_kzalloc(&pdev->dev, sizeof(*accel_priv), GFP_KERNEL);
	accel_priv->watermark = 1;
	init_completion(&accel_priv->kfifo_at_wm);

	rval = device_property_read_u32(&pdev->dev,"rohm,fifo-size",
					&accel_priv->fifo_size);

	if (rval != 0) {
		dev_err_probe(&pdev->dev, rval, "Device tree property "
						"rohm,fifo-size is missing!\n");
	}

	rval = kfifo_alloc(&accel_priv->kfifo_accel, FIFO_SIZE, GFP_KERNEL);

	if (rval != 0)
		dev_err(&pdev->dev, "Cannot allocate kfifo, errno: %d\n", rval);

	dev_set_drvdata(&pdev->dev, accel_priv);

	accel_priv->channel = devm_iio_channel_get_all(&pdev->dev);

	if (IS_ERR(accel_priv->channel)) {
		dev_info(&pdev->dev, "devm_iio_channel_get_all()  error\n");
		rval = PTR_ERR(accel_priv->channel);
		dev_info(&pdev->dev, "Error code: %d ", rval);
	}

	accel_priv->buffer = iio_channel_get_all_cb(&pdev->dev,&cb, accel_priv);

	if (IS_ERR(accel_priv->buffer)) {
		dev_info(&pdev->dev, "iio_channel_get_all_cb()  error\n");
		rval = PTR_ERR(accel_priv->buffer);
		dev_info(&pdev->dev, "Error code: %d ", rval);
	}
	dev_info(&pdev->dev, "end of probe\n");

	return rval;
}

static void test_cleanup_buffer(void *d)
{
	struct iio_cb_buffer *g_buf = (struct iio_cb_buffer *)d;

	pr_info("iio_channel_stop_all_cb called!\n");
	iio_channel_stop_all_cb(g_buf);
	iio_channel_release_all_cb(g_buf);
}

static void generic_accel_test_remove(struct platform_device *pdev)
{
	int ret;
	struct accel_priv *accel_priv = dev_get_drvdata(&pdev->dev);

	ret = devm_add_action_or_reset(&pdev->dev, &test_cleanup_buffer,
				       accel_priv->buffer);
}

static const struct of_device_id generic_accel_test_of_match[] = {
	{
		.compatible = "test,generic_accel",
	},
	{ }
};
MODULE_DEVICE_TABLE(of, generic_accel_test_of_match);

static struct platform_driver generic_accel_test_struct = {
	.probe = generic_accel_test_probe,
	.remove = generic_accel_test_remove,
	.driver = {
		.name = "test_module_kx022acr-z",
		.probe_type = PROBE_PREFER_ASYNCHRONOUS,
		.of_match_table = generic_accel_test_of_match,
		.dev_groups = generic_accel_test_attr_groups
	},
};

module_platform_driver(generic_accel_test_struct);

MODULE_AUTHOR("Kalle Niemi");
MODULE_DESCRIPTION("platform device test");
MODULE_LICENSE("GPL");
