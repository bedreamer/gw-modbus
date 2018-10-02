# -*- coding: utf8 -*-
import time
import httpd.SelectLoop as ioloop
import httpd.thttpd as web
import view


if __name__ == '__main__':
    loop = ioloop.get_select_loop()
    httpd = web.Httpd(iface='0.0.0.0', port=8080)
    httpd.start()

    httpd.route("^/can/usbcan/supported/$", view.get_supported_usbcan_list)

    httpd.route("^/can/usbcan/open/$", view.open_usbcan_device)
    httpd.route("^/can/usbcan/close/$", view.close_usbcan_device)
    httpd.route("^/can/usbcan/bps/$", view.get_supported_bps_list)

    httpd.route("^/can/usbcan/channel/open/$", view.open_usbcan_channel)
    httpd.route("^/can/usbcan/channel/close/$", view.close_usbcan_channel)

    while True:
        loop.run_step_forward()
        time.sleep(0.005)
