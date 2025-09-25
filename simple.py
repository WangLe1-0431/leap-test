"""
Author: WangLe1_
Email: leiw5385@gmail.com
Date: 2025-09-25
"""
import time
import leap

# 1) 定义一个很短的监听器（只关心连接和跟踪事件）
class SimpleListener(leap.Listener):
    def on_connection_event(self, event):
        # 当与 Leap Service 建立连接时会调用
        print("✅ 已连接到 Leap Service")

    def on_device_event(self, event):
        # 发现设备（可选，运行一次）
        try:
            with event.device.open():
                info = event.device.get_info()
        except Exception:
            info = event.device.get_info()
        print(f"🔌 设备: {info.serial}")

    def on_tracking_event(self, event):
        # 每次有跟踪帧到来时会被调用
        # event.tracking_frame_id 是帧编号
        # event.hands 是本帧检测到的手列表
        print(f"帧 {event.tracking_frame_id}，检测到 {len(event.hands)} 只手")
        for hand in event.hands:
            # hand.palm.position 是一个 vector，包含 x,y,z
            p = hand.palm.position
            # 输出格式简单明了，保留两位小数
            print(f"  手 ID={hand.id}，手掌坐标: x={p.x:.2f}, y={p.y:.2f}, z={p.z:.2f}")


def main():
    listener = SimpleListener()        # 创建监听器实例
    conn = leap.Connection()           # 创建与 Leap 的连接对象
    conn.add_listener(listener)        # 把监听器注册到连接上

    print("▶ 打开连接并开始跟踪（按 Ctrl+C 停止）")
    # 用 with context 打开连接，官方 example 就是这样用的
    try:
        with conn.open():
            # 明确设置 tracking mode（按你场景选 Desktop 或 VR）
            conn.set_tracking_mode(leap.TrackingMode.Desktop)
            # 主线程只需等待，回调会异步打印帧数据
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 用户停止")
    finally:
        # 移除监听器（安全清理）
        try:
            conn.remove_listener(listener)
        except Exception:
            pass
        print("退出。")


if __name__ == "__main__":
    main()
