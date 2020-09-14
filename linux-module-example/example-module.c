
#include <asm/uaccess.h>
#include <linux/delay.h>
#include <linux/fs.h>
#include <linux/gpio.h>
#include <linux/init.h>
#include <linux/interrupt.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/printk.h>

static __init int my_module_init(void)
{
        printk("my_module_init()\n");

	void b(void);
	b();
        return 0;
}

static __exit void my_module_exit(void)
{
	printk("my_module_exit()\n");
}

device_initcall_sync(my_module_init);
module_exit(my_module_exit);

MODULE_DESCRIPTION("my module");
MODULE_LICENSE("GPL v2");
