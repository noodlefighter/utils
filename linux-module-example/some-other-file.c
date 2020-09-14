#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/printk.h>

void b(void)
{
	printk("b()\n");
}

MODULE_LICENSE("GPL v2");
