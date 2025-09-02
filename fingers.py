# 中文节点监听 demo
import time
import leap
import csv

class 中文节点监听器(leap.Listener):
    """监听器：打印每帧手指关键节点（靠近手掌=1, 中间=2, 指尖=3）坐标，并保存到 CSV"""
    def __init__(self, csv_file="hand_tracking_nodes.csv"):
        super().__init__()
        self.csv_file = csv_file

        # 手指和节点名称
        self.手指名称 = ["拇指", "食指", "中指", "无名指", "小指"]
        self.节点名称 = ["关节1(靠近手掌)", "关节2(中间)", "关节3(指尖)"]

        # 初始化 CSV 文件
        with open(self.csv_file, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "frame_id", "hand_id", "手类型",
                "finger_id", "finger_name",
                "node_id", "node_name",
                "x", "y", "z"
            ])

    def on_connection_event(self, event):
        print("✅ 已连接 Leap 服务")

    def on_device_event(self, event):
        try:
            with event.device.open():
                info = event.device.get_info()
        except Exception:
            info = event.device.get_info()
        print(f"🔌 检测到设备: {info.serial}")

    def on_tracking_event(self, event):
        print(f"帧 {event.tracking_frame_id}，检测到 {len(event.hands)} 只手")

        for hand in event.hands:
            手类型 = "左手" if str(hand.type) == "HandType.Left" else "右手"
            print(f"  手 ID={hand.id}, 类型={手类型}")

            for digit in hand.digits:
                finger_name = self.手指名称[digit.finger_id]

                # 三个节点坐标
                节点坐标 = [
                    digit.bones[1].prev_joint,   # 关节1（靠近手掌）
                    digit.bones[2].prev_joint,   # 关节2（中间）
                    digit.bones[3].next_joint    # 关节3（指尖）
                ]

                for node_id, node_pos in enumerate(节点坐标):
                    node_name = self.节点名称[node_id]
                    print(f"    {finger_name} {node_name}: x={node_pos.x:.2f}, y={node_pos.y:.2f}, z={node_pos.z:.2f}")

                    # 写入 CSV
                    with open(self.csv_file, mode="a", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow([
                            event.tracking_frame_id,
                            hand.id,
                            手类型,
                            digit.finger_id,
                            finger_name,
                            node_id+1,
                            node_name,
                            f"{node_pos.x:.2f}",
                            f"{node_pos.y:.2f}",
                            f"{node_pos.z:.2f}"
                        ])

def main():
    监听器 = 中文节点监听器("hand_tracking_nodes.csv")
    连接 = leap.Connection()
    连接.add_listener(监听器)

    print("▶ 打开连接并开始跟踪（按 Ctrl+C 停止）")
    try:
        with 连接.open():
            连接.set_tracking_mode(leap.TrackingMode.Desktop)
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 用户停止")
    finally:
        try:
            连接.remove_listener(监听器)
        except Exception:
            pass
        print("退出。")

if __name__ == "__main__":
    main()
