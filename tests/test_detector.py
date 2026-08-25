from archpilot.detector import classify_gpu_vendor


def test_nvidia_detection():
    line = (
        "01:00.0 VGA compatible controller: "
        "NVIDIA Corporation RTX 4070"
    )

    assert classify_gpu_vendor(line) == "NVIDIA"

def test_amd_detection():
    line = (
        "03:00.0 VGA compatible controller: "
        "Advanced Micro Devices, Inc. AMD Radeon"
    )

    assert classify_gpu_vendor(line) == "AMD"

def test_intel_detectino():
    line = (
        "00:02.0 VGA compatible controler: "
        "Intel Corporation Graphics"
    )

    assert classify_gpu_vendor(line) == "Intel"