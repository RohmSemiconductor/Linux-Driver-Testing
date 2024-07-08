#include <linux/module.h>
#include <linux/platform_device.h>


static const struct of_device_id kalle_pd_of_match[] = {
	{
		.compatible = "kalle,kalle_pd",
	},
	{ }
};
MODULE_DEVICE_TABLE(of, kale_pd_of_match);

static int kalle_probe(struct platform_device *pdev)
{
	printk(KERN_INFO "Probe print\n");
	return 0;
}

static struct platform_driver kalle_pd_struct = {
	.driver = {
		.name = "test_module_kalle",
		.probe_type = PROBE_PREFER_ASYNCHRONOUS,
	},
	.probe = kalle_probe
};

module_platform_driver(kalle_pd_struct);

MODULE_AUTHOR("Kalle Niemi");
MODULE_DESCRIPTION("platform device test");
MODULE_LICENSE("GPL");
