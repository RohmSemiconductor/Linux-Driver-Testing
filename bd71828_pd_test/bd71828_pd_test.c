#include <linux/module.h>
#include <linux/platform_device.h>
#include <linux/of.h>
#include <linux/sysfs.h>
#include <linux/regulator/consumer.h>

struct regulator *g_r[14]={0};

static ssize_t vdd_en_show (struct kobject *ko, struct kobj_attribute *a, char *b)
{
	int rval;
	struct regulator *r = g_r[0];
	*b = (regulator_is_enabled(r))?'1':'0';
	b[1]='\0';
	rval=2;
	return rval;
}

static ssize_t vdd_en_store (struct kobject *ko, struct kobj_attribute *a, const char *b, size_t c)
{
	int rval = -EINVAL;
	struct regulator *r = g_r[0];

	if (*b == '1') {
		pr_info("Enabling vdd\n");
		rval = regulator_enable(r);
		if (rval){
			pr_info("Enabling vdd errno: %d\n", rval);
		}
	}
	if (*b == '0') {
		pr_info("Disabling vdd\n");
		rval = regulator_disable(r);
		if (rval){
			pr_info("Enabling vdd errno: %d\n", rval);
		}
	}
	rval = c;
	return rval;
}

static struct kobj_attribute vdd_en = __ATTR_RW(vdd_en);

static struct attribute *kalle_pd_reguattrs[] = {
	&vdd_en.attr,
	NULL		
};

static const struct attribute_group kalle_pd_attrs[] = {
	{
		.name = "regulators",
		.attrs = &kalle_pd_reguattrs[0],
	}
};

static const struct attribute_group *kalle_pd_attr_groups[] = {
	kalle_pd_attrs,
	NULL
};
/*
static struct kobject *g_k = NULL;
*/
/*
static int create_sysfs_kalle_pd(void)
{
	int retval;
	g_k = kobject_create_and_add("kalle_pd", kernel_kobj);
	retval = sysfs_create_group(g_k, &kalle_pd_attrs[0]);

	return retval;
}
*/
static int kalle_probe(struct platform_device *pdev)
{
	int retval = 0;
	dev_info(&pdev->dev, "Probe print\n");
/*	retval = create_sysfs_kalle_pd();*/
	g_r[0] = regulator_get(&pdev->dev, "vdd");

	if (IS_ERR(g_r[0])) {
		dev_info(&pdev->dev, "regulator_get error, vdd\n");
		retval = PTR_ERR(g_r[0]);
		dev_info(&pdev->dev, "Error code: %d ", retval);
	}

	g_r[1] = regulator_get(&pdev->dev, "vio");

	if (IS_ERR(g_r[1])) {
		dev_info(&pdev->dev, "regulator_get error, vio:\n");
		retval = PTR_ERR(g_r[1]);
		dev_info(&pdev->dev, "Error code: %d ", retval);
	}
	return retval;
}

static void kalle_probe_remove(struct platform_device *pdev)
{

}
static const struct of_device_id kalle_pd_of_match[] = {
	{
		.compatible = "kalle,kalle_pd",
	},
	{ }
};
MODULE_DEVICE_TABLE(of, kalle_pd_of_match);

static struct platform_driver kalle_pd_struct = {
	.probe = kalle_probe,
	.remove_new = kalle_probe_remove,
	.driver = {
		.name = "test_module_kalle",
		.probe_type = PROBE_PREFER_ASYNCHRONOUS,
		.of_match_table = kalle_pd_of_match,
		.dev_groups = kalle_pd_attr_groups
	},
};

module_platform_driver(kalle_pd_struct);

MODULE_AUTHOR("Kalle Niemi");
MODULE_DESCRIPTION("platform device test");
MODULE_LICENSE("GPL");
