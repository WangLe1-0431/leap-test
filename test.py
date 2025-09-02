# demo_working.py
import time
import leap

class PrintListener(leap.Listener):
    def on_connection_event(self, event):
        print("✅ Connected to Leap Service")

    def on_device_event(self, event):
        # 可选：打印设备信息 (不会每帧都打印)
        try:
            with event.device.open():
                info = event.device.get_info()
        except Exception:
            info = event.device.get_info()
        print(f"Found device {info.serial}")

    def on_tracking_event(self, event):
        # event.tracking_frame_id 和 event.hands 与官方 example 保持一致
        print(f"Frame {event.tracking_frame_id} with {len(event.hands)} hands.")
        for hand in event.hands:
            # hand.type 可能是枚举对象或字符串，下面兼容两种写法
            hand_type = "left" if getattr(hand, "type", str(hand.type)).name.lower() == "left" else "right" \
                if hasattr(hand, "type") else ("left" if str(hand.type).lower().find("left") >= 0 else "right")
            palm = hand.palm.position
            print(
                f"  Hand id {hand.id} ({hand_type}) palm: "
                f"({palm.x:.2f}, {palm.y:.2f}, {palm.z:.2f})"
            )

def main():
    listener = PrintListener()
    conn = leap.Connection()
    conn.add_listener(listener)

    print("▶ Opening connection and starting tracking...")
    try:
        # 用 with context 打开连接（官方 example 用法）
        with conn.open():
            # 明确设置 tracking mode（与 example 一致，Desktop/VR 等按你的设备场景）
            conn.set_tracking_mode(leap.TrackingMode.Desktop)
            print("Tracking started. Put your hand over the device (30-50cm). Press Ctrl+C to stop.")
            # 主循环：让 Listener 异步打印事件（不要在这里调用 poll）
            while True:
                time.sleep(1)  # 主线程只需要空转等待，Listener 会被回调
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")
    finally:
        try:
            conn.remove_listener(listener)
        except Exception:
            pass
        print("Listener removed, exiting.")

if __name__ == "__main__":
    main()
