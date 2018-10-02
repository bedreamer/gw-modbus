# -*- coding: utf8 -*-
import time
import gateway.can.api as api
import handle


def json_ok_result(request, data, **kwargs):
    return dict({
        "status": 'ok',
        "api": request.url,
        "data": data,
        "tsp": time.strftime('%Y-%m-%d %H:%M:%S')
    }, **kwargs)


def json_err_result(request, reason, **kwargs):
    return dict({
        "status": 'error',
        "reason": reason,
        "api": request.url,
        "tsp": time.strftime('%Y-%m-%d %H:%M:%S')
    }, **kwargs)


def json_device_model_unsupported(request, model):
    reason = "".join(["型号不支持(", model, ")"])
    return json_err_result(request, reason)


def json_need_correct_parameters(request, name):
    reason = "".join(["需要正确的`", name, "`参数"])
    return json_err_result(request, reason)


def json_invalid_handle_value(request, error_handle_value):
    reason = "".join(["handle value invalid`", str(error_handle_value), "`"])
    return json_err_result(request, reason)


def get_supported_usbcan_list(request):
    """
    curl http://{{ip}}/can/usbcan/supported/
    :param request:
    :return:
    """
    driver = api.get_supported_model_list()
    return {
        "status": "ok",
        "tsp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "data": driver
    }


def open_usbcan_device(request):
    """
    curl http://{{ip}}/can/usbcan/open/?{{model}}
    :param request:
    :return:
    """
    try:
        model = request.query.model
    except:
        return json_need_correct_parameters(request, 'model')

    try:
        dev_idx = int(request.query.dev_idx)
    except:
        dev_idx = 0

    try:
        driver = api.get_device_driver_by_model(model)
    except:
        return json_device_model_unsupported(request, model)

    try:
        device_handle = api.open_device(driver.model_type, dev_idx)
    except Exception as e:
        return json_err_result(request, str(e))

    if device_handle in {-1, 0, None}:
        return json_err_result(request, "设备打开失败")
    else:
        return json_ok_result(request, device_handle, model=model)


def close_usbcan_device(request):
    try:
        device_handle = int(request.query.device_handle)
    except:
        return json_need_correct_parameters(request, 'device_handle')

    if not handle.test(device_handle):
        return json_invalid_handle_value(request, device_handle)

    api.close_device(device_handle)
    return json_ok_result(request, -1)


def get_supported_bps_list(request):
    try:
        model = request.query.model
    except:
        return json_need_correct_parameters(request, 'model')

    bps_list = api.get_device_bps_by_model(model)
    return json_ok_result(request, list(bps_list))


def open_usbcan_channel(request):
    """
    打开通道
    :param request:
    :return:
    """
    try:
        device_handle = int(request.query.device_handle)
    except:
        return json_need_correct_parameters(request, 'device_handle')

    try:
        channel_number = int(request.query.channel_number)
    except:
        channel_number = 0

    try:
        bps = request.query.bps
        if bps not in api.get_device_bps_by_device_handle(device_handle):
            raise ValueError
    except:
        return json_need_correct_parameters(request, 'bps')

    try:
        work_mode = int(request.query.work_mode)
    except:
        work_mode = 0

    if not handle.test(device_handle):
        return json_invalid_handle_value(request, device_handle)

    channel_handle = api.open_channel(device_handle, channel_number, bps, work_mode)
    return json_ok_result(request, channel_handle, device_handle=device_handle, bps=bps, work_mode=work_mode)


def close_usbcan_channel(request):
    """
    关闭通道
    :param request:
    :return:
    """
    try:
        channel_handle = int(request.query.channel_handle)
    except:
        return json_need_correct_parameters(request, 'channel_handle')

    if not handle.test(channel_handle):
        return json_invalid_handle_value(request, channel_handle)

    api.close_channel(channel_handle)
    return json_ok_result(request, -1)

