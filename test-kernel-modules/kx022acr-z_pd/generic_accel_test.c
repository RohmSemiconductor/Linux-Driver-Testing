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

struct iio_channel *g_chan;
struct iio_cb_buffer *g_buf;

struct scan {
	__le16 channels[3];
	s64 ts __aligned(8);
};

struct accel_priv {
	struct scan *scan;
};

struct accel_priv cb_priv;

struct accel_test {
	unsigned int watermark;
};

struct accel_test g_accel_test;

const unsigned int ms2_mult = 1000;

enum INT_TO_FRAC {
	INT_TO_FRAC_MICRO = 6,
	INT_TO_FRAC_NANO = 9
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

static ssize_t x_buffer_show (struct kobject *ko, struct kobj_attribute *a, char *b)
{
	int rval;
	struct iio_cb_buffer *buff = g_buf;

	rval = iio_channel_start_all_cb(buff);
	pr_info("iio_channel_start_all_cb called!\n");

	rval = sprintf(b, "%d\n", cb_priv.scan->channels[0]);

	return rval;
}

static struct kobj_attribute x_buffer = __ATTR_RO(x_buffer);

static ssize_t y_buffer_show (struct kobject *ko, struct kobj_attribute *a, char *b)
{
	int rval;
	struct iio_cb_buffer *buff = g_buf;

	rval = iio_channel_start_all_cb(buff);
	pr_info("iio_channel_start_all_cb called!\n");

	rval = sprintf(b, "%d\n", cb_priv.scan->channels[1]);

	return rval;
}

static struct kobj_attribute y_buffer = __ATTR_RO(y_buffer);

static ssize_t z_buffer_show (struct kobject *ko, struct kobj_attribute *a, char *b)
{
	int rval;
	struct iio_cb_buffer *buff = g_buf;

	rval = iio_channel_start_all_cb(buff);
	pr_info("iio_channel_start_all_cb called!\n");

	if (rval != 0)
		pr_err("iio_channel_start_all_cb: %d\n", rval);

	rval = sprintf(b, "%d\n", cb_priv.scan->channels[2]);

	return rval;
}

static struct kobj_attribute z_buffer = __ATTR_RO(z_buffer);

static ssize_t buffer2list_show (struct kobject *ko, struct kobj_attribute *a, char *b)
{
	int rval;
	return rval;
}
static ssize_t buffer2list_store (struct kobject *ko, struct kobj_attribute *a, const char *b, size_t c)
{
	int rval;

	return rval;
}

static struct kobj_attribute buffer2list = __ATTR_RW(buffer2list);

static ssize_t read_buffer_show (struct kobject *ko, struct kobj_attribute *a, char *b)
{
	int rval;

	rval = sprintf(b, "%d\n", sizeof(*b));
	rval += sprintf(b + rval, "%d\n", sizeof(*b));

	return rval;
}
static ssize_t read_buffer_store (struct kobject *ko, struct kobj_attribute *a, const char *b, size_t c)
{
	int rval = -EINVAL;
	unsigned int watermark;
	char axis[2];
	int xyz_match;

	struct iio_cb_buffer *buff = g_buf;

	iio_channel_stop_all_cb(buff);
	pr_info("iio_channel_stop_all_cb called!\n");

	if (2 == sscanf(b, "%s %d", axis, &watermark))
	{
		rval = iio_channel_cb_set_buffer_watermark(buff,watermark);
		if (rval != 0)
			pr_err("watermark error: %d\n", rval);
		else
			g_accel_test.watermark = watermark;

	}
	else if (1 == sscanf(b,"%s", axis))
	{
		xyz_match = !(!strncmp(axis, "x", 2) ^ !strncmp(axis, "y", 2) ^ !strncmp(axis, "z", 2));
		pr_info("xyz_match: %d\n", xyz_match);

		if (xyz_match == 0)
		{
			pr_info("if or or sisalla\n");
			watermark = g_accel_test.watermark;
			rval = iio_channel_cb_set_buffer_watermark(buff,watermark);
		}
		else
			pr_info("%d",strncmp(axis, "x",2));
	}
	else
		pr_err("sscanf return: %d\n", rval);

	if (!rval)
	{
		pr_info("okei, nyt ollaan !rvalissa\n");
		rval = iio_channel_start_all_cb(buff);
		pr_info("iio_channel_start_all_cb called!\n");

		for (int x = 0; x < g_accel_test.watermark; x++)
		{
			pr_info("for loopissa: %d\n",x);
			if (strncmp(axis, "x",1) == 0)
			{
				/* This does not get new values */
				pr_info("%d\n", cb_priv.scan->channels[0]);
			}
		}
	}

	rval = c;
	return rval;
}

static struct kobj_attribute read_buffer = __ATTR_RW(read_buffer);


static ssize_t scale_available_show (struct kobject *ko, struct kobj_attribute *a, char *b)
{
	int rval;
	struct iio_channel *chan = g_chan;
	int type;
	int length;
	const int *list_vals;
	const int **vals = &list_vals;
	char freq_avail[100];
	char fval[15];

	rval = iio_read_avail_channel_attribute(chan, vals, &type, &length, IIO_CHAN_INFO_SCALE);

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

static struct kobj_attribute scale_available = __ATTR_RO(scale_available);

static ssize_t sampling_frequency_available_show (struct kobject *ko, struct kobj_attribute *a, char *b)
{
	int rval;
	struct iio_channel *chan = g_chan;
	int type;
	int length;
	const int *list_vals;
	const int **vals = &list_vals;
	char freq_avail[100];
	char fval[15];
//	rval = g_chan->indio_dev->info->read_avail(g_chan->indio_dev,g_chan->indio_dev->channels,vals,IIO_VAL_INT_PLUS_MICRO);

	rval = iio_read_avail_channel_attribute(chan, vals, &type, &length, IIO_CHAN_INFO_SAMP_FREQ);

	if (rval < 0) {
		pr_err("Problems reading available sampling frequencies! Errno: %d", rval);
		return rval;
	}
//	rval = sprintf(b, "type: %d, length: %d\n", type, length);

	for (int x=0; x < length; x=x+2) {
		sprintf(fval, "%d.", vals[0][x]);
		strcat(freq_avail,fval);
		sprintf(fval, "%d ", vals[0][x+1]);
		strcat(freq_avail, fval);
	}
	rval = sprintf(b,"%s\n", freq_avail);
	return rval;
}

static struct kobj_attribute sampling_frequency_available = __ATTR_RO(sampling_frequency_available);

static ssize_t hwfifo_watermark_show (struct kobject *ko, struct kobj_attribute *a, char *b)
{
	int rval;

	rval = sprintf(b, "Write only\n");
	pr_info("Write only\n");


	return rval;
}

static ssize_t hwfifo_watermark_store (struct kobject *ko, struct kobj_attribute *a, const char *b, size_t c)
{
	int rval;
	struct iio_channel *chan = g_chan;
	size_t watermark;

	rval = sscanf(b, "%d", &watermark);

	rval = chan->indio_dev->info->hwfifo_set_watermark(chan->indio_dev, watermark);

	if (rval < 0)
		pr_err("watermark error: %d\n", rval);

	rval = c;
	return rval;
}

static struct kobj_attribute hwfifo_watermark = __ATTR_RW(hwfifo_watermark);


static ssize_t watermark_show (struct kobject *ko, struct kobj_attribute *a, char *b)
{
	int rval;

	rval = sprintf(b, "%d\n", g_accel_test.watermark);
	pr_info("write only\n");

	return rval;
}

static ssize_t watermark_store (struct kobject *ko, struct kobj_attribute *a, const char *b, size_t c)
{
	int rval;
	unsigned int watermark;
	struct iio_cb_buffer *buff = g_buf;

	iio_channel_stop_all_cb(buff);
	pr_info("iio_channel_stop_all_cb called!\n");

	rval = sscanf(b, "%d", &watermark);

	rval = iio_channel_cb_set_buffer_watermark(buff,watermark);
	pr_info("iio_channel_cb_set_buffer_watermark called!\n");

	pr_info("watermark_store rval: %d\n",rval);

	if (rval != 0)
		pr_err("watermark error: %d\n", rval);
	else
		g_accel_test.watermark = watermark;

	rval = iio_channel_start_all_cb(buff);
	pr_info("iio_channel_start_all_cb called!\n");

	if (rval != 0)
		pr_err("iio_channel_start_all_cb: %d\n", rval);

	iio_channel_stop_all_cb(buff);
	pr_info("iio_channel_stop_all_cb called!\n");

	rval = c;
	return rval;
}

static struct kobj_attribute watermark = __ATTR_RW(watermark);


static ssize_t sampling_frequency_show (struct kobject *ko, struct kobj_attribute *a, char *b)
{
	int rval;
	struct iio_channel *chan = g_chan;
	int val;
	int val2;

	rval = iio_read_channel_attribute(chan, &val, &val2, IIO_CHAN_INFO_SAMP_FREQ);
	if (val < 0)
		pr_err("iio_read_channel_attribute errno %d\n", rval);

	rval = sprintf(b, "%d.%06d\n", val, val2);

	return rval;
}

static ssize_t sampling_frequency_store (struct kobject *ko, struct kobj_attribute *a, const char *b, size_t c)
{
	struct iio_channel *chan = g_chan;
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
			pr_err("Dont put stuff where it does not belong! Error: %d\n", val2);
			return val2;
		}
	}

	rval = iio_write_channel_attribute(chan, val, val2, IIO_CHAN_INFO_SAMP_FREQ);

	if (rval < 0)
	{
		pr_err("SAMP_FREQ: iio_write_channel_attribute errno %d\n", rval);
		return rval;
	}

	pr_info("Sampling frequency set to: %d.%d\n", val, val2);
	rval = c;
	return rval;
}

static struct kobj_attribute sampling_frequency = __ATTR_RW(sampling_frequency);

static ssize_t scale_show (struct kobject *ko, struct kobj_attribute *a, char *b)
{
	int rval;
	int val;
	int val2;
	struct iio_channel *chan = g_chan;

	rval = iio_read_channel_attribute(chan, &val, &val2, IIO_CHAN_INFO_SCALE);
	if (rval < 0)
		pr_err("SCALE: iio_read_channel_attribute errno %d\n", rval);
	rval = sprintf(b, "%d.%09d\n", val, val2);

	return rval;
}

static ssize_t scale_store (struct kobject *ko, struct kobj_attribute *a, const char *b, size_t c)
{
	int rval;
	int val;
	int val2;
	char val2_buffer[10];
	struct iio_channel *chan = g_chan;

	rval = sscanf(b, "%d.%9s", &val, val2_buffer);

	val2 = char_to_frac(val2_buffer, INT_TO_FRAC_NANO);
	if (val2 < 0 ) {
		pr_err("Dont put stuff where it does not belong! Error: %d\n", val2);
		return val2;
	}

	rval = iio_write_channel_attribute(chan, val, val2, IIO_CHAN_INFO_SCALE);

	if (rval < 0)
	{
		pr_err("iio_write_channel_attribute errno %d\n", rval);
		return rval;
	}

	pr_info("Scale written: %d.%d\n", val, val2);

	rval = c;
	return rval;
}

static struct kobj_attribute scale = __ATTR_RW(scale);

static ssize_t x_raw_show (struct kobject *ko, struct kobj_attribute *a, char *b)
{
	int rval;
	int val;
	struct iio_channel *chan = g_chan;
	struct iio_cb_buffer *buff = g_buf;

	iio_channel_stop_all_cb(buff);
	pr_info("iio_channel_stop_all_cb called!\n");

	rval = iio_read_channel_raw(&chan[0], &val );

	if (rval < 0)
		pr_err("iio_read_channel_raw errno: %d\n", rval);

	rval = sprintf(b,"%d\n",val);

	return rval;
}

static struct kobj_attribute x_raw = __ATTR_RO(x_raw);

static ssize_t y_raw_show (struct kobject *ko, struct kobj_attribute *a, char *b)
{
	int rval;
	struct iio_channel *chan = g_chan;
	struct iio_cb_buffer *buff = g_buf;
	int val;

	iio_channel_stop_all_cb(buff);
	pr_info("iio_channel_stop_all_cb called!\n");

	rval = iio_read_channel_raw(&chan[1], &val );

	if (rval < 0)
		pr_err("iio_read_channel_raw errno: %d\n", rval);

	rval = sprintf(b,"%d\n",val);

	return rval;
}

static struct kobj_attribute y_raw = __ATTR_RO(y_raw);

static ssize_t z_raw_show (struct kobject *ko, struct kobj_attribute *a, char *b)
{
	int rval;
	struct iio_channel *chan = g_chan;
	struct iio_cb_buffer *buff = g_buf;
	int val;

	iio_channel_stop_all_cb(buff);
	pr_info("iio_channel_stop_all_cb called!\n");

	rval = iio_read_channel_raw(&chan[2], &val );

	if (rval < 0)
		pr_err("iio_read_channel_raw errno: %d\n", rval);

	rval = sprintf(b,"%d\n",val);

	return rval;
}

static struct kobj_attribute z_raw = __ATTR_RO(z_raw);

static ssize_t x_ms2_show (struct kobject *ko, struct kobj_attribute *a, char *b)
{
	int rval;
	struct iio_channel *chan = g_chan;
	int val;
	int value1;
	int value2;

	rval = iio_read_channel_processed_scale(&chan[0], &val, ms2_mult);

	if (rval < 0)
		pr_err("iio_read_channel_raw errno: %d\n", val);

	pscale_split_to_ints(val, ms2_mult, &value1, &value2);

	rval = sprintf(b,"%d.%d\n",value1, value2);

	return rval;
}

static struct kobj_attribute x_ms2 = __ATTR_RO(x_ms2);

static ssize_t y_ms2_show (struct kobject *ko, struct kobj_attribute *a, char *b)
{
	int rval;
	struct iio_channel *chan = g_chan;
	int val;
	int value1;
	int value2;

	rval = iio_read_channel_processed_scale(&chan[1], &val, ms2_mult);

	if (rval < 0)
		pr_err("iio_read_channel_raw errno: %d\n", val);

	pscale_split_to_ints(val, ms2_mult, &value1, &value2);

	rval = sprintf(b,"%d.%d\n",value1, value2);

	return rval;
}

static struct kobj_attribute y_ms2 = __ATTR_RO(y_ms2);

static ssize_t z_ms2_show (struct kobject *ko, struct kobj_attribute *a, char *b)
{
	int rval;
	struct iio_channel *chan = g_chan;
	int val;
	int value1;
	int value2;

	rval = iio_read_channel_processed_scale(&chan[2], &val, ms2_mult);

	if (rval < 0)
		pr_err("iio_read_channel_raw errno: %d\n", val);

	pscale_split_to_ints(val, ms2_mult, &value1, &value2);

	rval = sprintf(b,"%d.%d\n",value1, value2);

	return rval;
}

static struct kobj_attribute z_ms2 = __ATTR_RO(z_ms2);

static ssize_t timestamp_show (struct kobject *ko, struct kobj_attribute *a, char *b)
{
	int rval;
//	struct iio_channel *chan = g_chan;

	/*
	rval = iio_read_channel_raw(&chan[3], &val);

	if (rval < 0)
		pr_err("iio_read_channel_raw errno: %d\n", cb_priv.scan->ts);
	*/
	rval = sprintf(b,"%lld\n",cb_priv.scan->ts);

	return rval;
}
static struct kobj_attribute timestamp = __ATTR_RO(timestamp);

static struct attribute *test_kx022acr_z_chattrs[] = {
	&read_buffer.attr,
	&x_buffer.attr,
	&y_buffer.attr,
	&z_buffer.attr,
	&scale_available.attr,
	&sampling_frequency_available.attr,
	&hwfifo_watermark.attr,
	&watermark.attr,
	&sampling_frequency.attr,
	&scale.attr,
	&x_raw.attr,
	&y_raw.attr,
	&z_raw.attr,
	&x_ms2.attr,
	&y_ms2.attr,
	&z_ms2.attr,
	&timestamp.attr,
	NULL
};

static const struct attribute_group test_kx022acr_z_attrs[] = {
	{
		.name = "iio_channels",
		.attrs = &test_kx022acr_z_chattrs[0],
	}
};

static const struct attribute_group *test_kx022acr_z_attr_groups[] = {
	test_kx022acr_z_attrs,
	NULL
};

static int cb(const void *data, void *private)
{
/*
	struct scan {
		__le16 channels[3];
		s64 ts __aligned(8);
	};
*/
	struct scan *buf_data;

	buf_data = (struct scan*)data;

	cb_priv.scan = (struct scan*)data;

/*
	pr_info("CB FUNC CALLED!");

	pr_info("Chan0: %d\n", buf_data->channels[0]);
	pr_info("Chan1: %d\n", buf_data->channels[1]);
	pr_info("Chan2: %d\n", buf_data->channels[2]);
*/
	return 0;
}

static int test_kx022acr_z_probe(struct platform_device *pdev)
{
	int retval = 0;
	dev_info(&pdev->dev, "Ver 021\n");
	int vcb = 0;
	void *vcbp = &vcb;

	g_chan = devm_iio_channel_get_all(&pdev->dev);

	if (IS_ERR(g_chan)) {
		dev_info(&pdev->dev, "devm_iio_channel_get_all()  error\n");
		retval = PTR_ERR(g_chan);
		dev_info(&pdev->dev, "Error code: %d ", retval);
	}

	g_buf = iio_channel_get_all_cb(&pdev->dev,&cb,vcbp);

	if (IS_ERR(g_buf)) {
		dev_info(&pdev->dev, "iio_channel_get_all_cb()  error\n");
		retval = PTR_ERR(g_buf);
		dev_info(&pdev->dev, "Error code: %d ", retval);
	}


	retval = iio_channel_start_all_cb(g_buf);
	return retval;
}

static void test_cleanup_buffer(void *d)
{
	struct iio_cb_buffer *g_buf = (struct iio_cb_buffer *)d;

	pr_info("iio_channel_stop_all_cb called!\n");
	iio_channel_stop_all_cb(g_buf);
	iio_channel_release_all_cb(g_buf);
}

static void test_kx022acr_z_remove(struct platform_device *pdev)
{
	int ret;

	ret = devm_add_action_or_reset(&pdev->dev, &test_cleanup_buffer, g_buf);
}

static const struct of_device_id test_kx022acr_z_of_match[] = {
	{
		.compatible = "test,kx022acr-z",
	},
	{ }
};
MODULE_DEVICE_TABLE(of, test_kx022acr_z_of_match);

static struct platform_driver test_kx022acr_z_struct = {
	.probe = test_kx022acr_z_probe,
	.remove = test_kx022acr_z_remove,
	.driver = {
		.name = "test_module_kx022acr-z",
		.probe_type = PROBE_PREFER_ASYNCHRONOUS,
		.of_match_table = test_kx022acr_z_of_match,
		.dev_groups = test_kx022acr_z_attr_groups
	},
};

module_platform_driver(test_kx022acr_z_struct);

MODULE_AUTHOR("Kalle Niemi");
MODULE_DESCRIPTION("platform device test");
MODULE_LICENSE("GPL");
