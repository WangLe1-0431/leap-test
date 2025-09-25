# 这是一个用于学习leapmotion的测试项目

# Leap Motion 手部追踪示例文档

本文档说明如何运行本仓库中的示例脚本，并展示数据含义与常见问题处理。文件使用 UTF-8 编码与标准 Markdown 语法，确保在 GitHub、VS Code 及常见编辑器中正确显示。

## 环境要求

- Python 3.8+
- Leap Motion/Ultraleap Tracking SDK（已安装并启动服务）
- Windows/macOS/Linux，终端可运行 `python`

## 快速开始

```bash
python fingers.py
```

运行后：

- 终端会打印每帧每根手指的三个关键节点坐标。
- 同时会将数据追加写入 `hand_tracking_nodes.csv`。

## 数据字段说明（CSV）


| 字段名      | 含义                      |
| ----------- | ------------------------- |
| frame_id    | 跟踪帧编号                |
| hand_id     | 手的唯一 ID               |
| hand_type   | 左手/右手                 |
| finger_id   | 手指 ID（0-拇指…4-小指） |
| finger_name | 手指中文名                |
| node_id     | 关节编号（1、2、3）       |
| node_name   | 关节中文名                |
| x           | X 坐标（毫米）            |
| y           | Y 坐标（毫米）            |
| z           | Z 坐标（毫米）            |

示例输出（终端）：

```text
帧 12345，检测到 1 只手
  手 ID=7, 类型=右手
    食指 关节1(靠近手掌): x=12.34, y=56.78, z=90.12
```

## 常见问题（显示/编码）

- 若中文显示为乱码，请确保文件保存为 UTF-8 编码。
  - VS Code：右下角编码选择“UTF-8”，如需可选“以 UTF-8 保存”。
  - Windows 记事本较老版本需要 UTF-8 BOM 才能正确识别，可改用 VS Code。
- 若 CSV 在 Excel 中中文显示异常：
  - 打开 Excel 后，使用“数据”→“自文本/CSV”导入，选择“UTF-8”编码。
- 终端显示 emoji 或中文异常：
  - 切换到支持 UTF-8 的终端/字体，或去掉输出中的 emoji。

## 相关脚本

- `fingers.py`：打印并记录手指关键节点坐标（已使用 UTF-8 与中文输出）。
- `simple.py` / `test.py`：简化/打印示例。

---

如需把本文档改为英文版、添加截图/流程图、或发布到 GitHub Pages，请告诉我，我可以继续完善格式与内容。
