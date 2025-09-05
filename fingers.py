#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
手指节点监听 demo（UTF-8，ASCII 标识符，中文输出）

- 打印每帧每根手指的 3 个关键节点坐标：
  关节1(靠近手掌)、关节2(中间)、关节3(指尖)
- 同步保存到 CSV 文件。

注意：原文件存在乱码与中文标识符，可能导致语法/编码错误。
本版本改为 ASCII 标识符并确保 UTF-8 编码，避免平台编码问题。
"""

import time
import csv
import leap


class ChineseFingerNodesListener(leap.Listener):
    def __init__(self, csv_file: str = "hand_tracking_nodes.csv"):
        super().__init__()
        self.csv_file = csv_file

        # 名称表（仅作为输出标签）
        self.finger_names_cn = ["拇指", "食指", "中指", "无名指", "小指"]
        self.node_names_cn = ["关节1(靠近手掌)", "关节2(中间)", "关节3(指尖)"]

        # 初始化 CSV 头
        with open(self.csv_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "frame_id",
                "hand_id",
                "hand_type",
                "finger_id",
                "finger_name",
                "node_id",
                "node_name",
                "x",
                "y",
                "z",
            ])

    # 连接事件
    def on_connection_event(self, event):
        print("已连接 Leap 服务")

    # 设备事件（打印序列号）
    def on_device_event(self, event):
        try:
            # 有些版本需要先 open 才能读到完整信息
            with event.device.open():
                info = event.device.get_info()
        except Exception:
            info = event.device.get_info()
        print(f"检测到设备: {info.serial}")

    # 跟踪事件（每帧回调）
    def on_tracking_event(self, event):
        print(f"帧 {event.tracking_frame_id}，检测到 {len(event.hands)} 只手")

        for hand in event.hands:
            hand_type = self._hand_type_cn(hand)
            print(f"  手 ID={hand.id}, 类型={hand_type}")

            for digit in hand.digits:
                finger_name = self._safe_finger_name(digit.finger_id)

                # 三个节点坐标
                node_positions = [
                    digit.bones[1].prev_joint,   # 关节1（靠近手掌）
                    digit.bones[2].prev_joint,   # 关节2（中间）
                    digit.bones[3].next_joint,   # 关节3（指尖）
                ]

                for node_id, node_pos in enumerate(node_positions, start=1):
                    node_name = self.node_names_cn[node_id - 1]
                    print(
                        f"    {finger_name} {node_name}: "
                        f"x={node_pos.x:.2f}, y={node_pos.y:.2f}, z={node_pos.z:.2f}"
                    )

                    # 写入 CSV（追加）
                    with open(self.csv_file, mode="a", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow([
                            event.tracking_frame_id,
                            hand.id,
                            hand_type,
                            digit.finger_id,
                            finger_name,
                            node_id,
                            node_name,
                            f"{node_pos.x:.2f}",
                            f"{node_pos.y:.2f}",
                            f"{node_pos.z:.2f}",
                        ])

    # 帮助函数：更稳妥地获取左右手
    @staticmethod
    def _hand_type_cn(hand) -> str:
        try:
            t = getattr(hand, "type", None)
            name = t.name if hasattr(t, "name") else str(hand.type)
            s = str(name).lower()
        except Exception:
            s = str(hand.type).lower()
        return "左手" if "left" in s else "右手"

    def _safe_finger_name(self, finger_id: int) -> str:
        try:
            return self.finger_names_cn[finger_id]
        except Exception:
            return f"手指{finger_id}"


def main():
    listener = ChineseFingerNodesListener("hand_tracking_nodes.csv")
    conn = leap.Connection()
    conn.add_listener(listener)

    print("打开连接并开始跟踪（按 Ctrl+C 停止）")
    try:
        with conn.open():
            conn.set_tracking_mode(leap.TrackingMode.Desktop)
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        print("\n用户停止")
    finally:
        try:
            conn.remove_listener(listener)
        except Exception:
            pass
        print("退出")


if __name__ == "__main__":
    main()

