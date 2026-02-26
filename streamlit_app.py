# # streamlit_app.py  (place in project root: C:\Defect detection using agentic ai)

# import sys
# import random
# import time
# from pathlib import Path

# import streamlit as st
# import pandas as pd
# from PIL import Image, ImageDraw

# # Make src/ importable
# PROJECT_ROOT = Path(__file__).resolve().parent
# SRC_DIR = PROJECT_ROOT / "src"
# sys.path.append(str(SRC_DIR))

# from conveyor_belt import generate_belt_frames   # uses your existing belt code
# from agents_graph import run_agents_on_frame     # the agent pipeline

# # ==========================================
# # CONFIG
# # ==========================================
# TEST_DEF = PROJECT_ROOT / "data" / "casting_data" / "test" / "def_front"
# TEST_OK  = PROJECT_ROOT / "data" / "casting_data" / "test" / "ok_front"

# PRODUCT_W = 90
# PRODUCT_H = 90
# PRODUCT_Y = 115  # y-position on belt (matches your earlier code)


# # ==========================================
# # LOAD 30 IMAGES (15 def + 15 ok, shuffled)
# # ==========================================
# def load_30_test_images():
#     def_files = list(TEST_DEF.glob("*.*"))
#     ok_files  = list(TEST_OK.glob("*.*"))

#     if len(def_files) < 15 or len(ok_files) < 15:
#         raise RuntimeError("Not enough test images to sample 15 from each class.")

#     random.shuffle(def_files)
#     random.shuffle(ok_files)

#     def_files = def_files[:15]
#     ok_files = ok_files[:15]

#     all_files = def_files + ok_files
#     random.shuffle(all_files)

#     images = []
#     for i, path in enumerate(all_files):
#         img = Image.open(path).convert("RGBA")
#         img = img.resize((PRODUCT_W, PRODUCT_H))
#         images.append({
#             "image_name": f"Image {i}",
#             "path": path,
#             "img": img,
#         })
#     return images


# # ==========================================
# # BELT FRAMES (re-use your conveyor animation frames)
# # ==========================================
# belt_frames = generate_belt_frames()  # from conveyor_belt.py
# BELT_COUNT = len(belt_frames)


# # ==========================================
# # DRAW BORDER + LABEL
# # ==========================================
# def add_border_and_label(frame: Image.Image,
#                          image_name: str,
#                          prediction: str,
#                          confidence: float,
#                          action: str):
#     img = frame.copy()
#     draw = ImageDraw.Draw(img)
#     w, h = img.size

#     # Color selection
#     if prediction == "OK" and action == "ACCEPT":
#         color = (0, 220, 0)      # green
#     elif prediction == "Defective" and action == "REJECT":
#         color = (220, 0, 0)      # red
#     else:
#         color = (255, 215, 0)    # yellow

#     # Border
#     border_th = 6
#     for i in range(border_th):
#         draw.rectangle([i, i, w - 1 - i, h - 1 - i], outline=color)

#     # Label box
#     text_lines = [
#         image_name,
#         f"Prediction: {prediction}",
#         f"Confidence: {confidence * 100:.1f}%",
#         f"Action: {action}",
#     ]
#     text = "\n".join(text_lines)

#     box_w = 340
#     box_h = 90
#     draw.rectangle([10, 10, 10 + box_w, 10 + box_h], fill=(0, 0, 0, 180))
#     draw.text((20, 20), text, fill=color)

#     return img


# # ==========================================
# # STREAMLIT UI
# # ==========================================
# st.set_page_config(
#     page_title="Agentic AI – Conveyor Defect Detection",
#     page_icon="🤖",
#     layout="wide",
# )

# st.markdown(
#     "<h1 style='text-align:center; color:#4CAF50;'>🏭 Agentic AI – Defect Detection on Conveyor Belt</h1>",
#     unsafe_allow_html=True,
# )
# st.markdown(
#     "<p style='text-align:center;'>Vision → Analysis → Decision → Report – all automated on 30 test images.</p>",
#     unsafe_allow_html=True,
# )

# st.markdown("---")

# left, right = st.columns([1.4, 1.6])

# with left:
#     st.subheader("🧪 Test Images (30)")
#     st.write("Randomly sampled: 15 Defective + 15 OK images, shuffled.")

#     try:
#         test_images = load_30_test_images()
#     except Exception as e:
#         st.error(f"Error loading test images: {e}")
#         st.stop()

#     # Preview thumbs
#     thumb_cols = st.columns(5)
#     for i, item in enumerate(test_images[:10]):  # show first 10 thumbnails
#         with thumb_cols[i % 5]:
#             st.image(item["img"], caption=item["image_name"], width=100)

# with right:
#     st.subheader("🤖 Agent Pipeline")
#     st.markdown("""
#     **Agents used:**
#     - 👁️ **Vision Agent** – receives the belt frame with product.
#     - 🧠 **Analysis Agent** – runs the ResNet18 model to classify: OK / Defective.
#     - ⚖️ **Decision Agent** – converts prediction into action: ACCEPT / REJECT.
#     - 📄 **Report Agent** – adds timestamp for inspection log.
#     """)

# st.markdown("---")

# st.subheader("🎥 Live Detection on Conveyor Belt")

# image_placeholder = st.empty()
# results = []

# if st.button("▶ Run Agentic Detection on 30 Images"):
#     for idx, item in enumerate(test_images):
#         # Pick belt frame (loop through belt animation)
#         belt = belt_frames[idx % BELT_COUNT].copy()

#         # Paste product at center of belt
#         product = item["img"]
#         bw, bh = belt.size
#         x = bw // 2 - PRODUCT_W // 2
#         y = PRODUCT_Y
#         belt.paste(product, (x, y), product)

#         image_name = item["image_name"]

#         # Run through agents
#         state = run_agents_on_frame(image_name=image_name, frame_id=idx, frame=belt)

#         prediction = state.get("prediction", "ERROR")
#         confidence = state.get("confidence", 0.0)
#         action = state.get("action", "ERROR")
#         timestamp = state.get("timestamp", "")

#         if state.get("error"):
#             prediction = "ERROR"
#             action = "ERROR"

#         # Draw border + label
#         display_frame = add_border_and_label(
#             belt, image_name, prediction, confidence, action
#         )

#         # Show frame
#         image_placeholder.image(
#             display_frame,
#             caption=f"{image_name} → {prediction} ({action})",
#             use_column_width=True,
#         )

#         # Log row
#         results.append({
#             "Image Name": image_name,
#             "Frame Number": idx,
#             "Prediction": prediction,
#             "Confidence": round(confidence, 4),
#             "Action": action,
#             "Timestamp": timestamp,
#         })

#         time.sleep(0.4)  # slow for demo

#     st.markdown("---")
#     st.subheader("📊 Final Inspection Report (30 Images)")

#     df = pd.DataFrame(results)
#     st.dataframe(df, use_container_width=True)

#     # Summary
#     total = len(df)
#     ok_count = (df["Prediction"] == "OK").sum()
#     defect_count = (df["Prediction"] == "Defective").sum()
#     error_count = (df["Prediction"] == "ERROR").sum()

#     st.markdown(f"""
#     - **Total images processed**: `{total}`
#     - ✅ **OK**: `{ok_count}`
#     - ❌ **Defective**: `{defect_count}`
#     - ⚠️ **Errors**: `{error_count}`
#     """)

#     # Download CSV
#     csv_bytes = df.to_csv(index=False).encode("utf-8")
#     st.download_button(
#         "⬇ Download Inspection Report (CSV)",
#         data=csv_bytes,
#         file_name="inspection_report_30_images.csv",
#         mime="text/csv",
#     )

# else:
#     st.info("Click **▶ Run Agentic Detection on 30 Images** to start the demo.")


#final code 
# import sys
# import random
# import time
# from pathlib import Path

# import streamlit as st
# import pandas as pd
# from PIL import Image, ImageDraw

# # Make src/ importable
# PROJECT_ROOT = Path(__file__).resolve().parent
# SRC_DIR = PROJECT_ROOT / "src"
# sys.path.append(str(SRC_DIR))

# from conveyor_belt import generate_belt_frames
# from agents_graph import run_agents_on_frame


# # ==========================================
# # CONFIG
# # ==========================================
# TEST_DEF = PROJECT_ROOT / "data" / "casting_data" / "test" / "def_front"
# TEST_OK  = PROJECT_ROOT / "data" / "casting_data" / "test" / "ok_front"

# PRODUCT_W = 90
# PRODUCT_H = 90
# PRODUCT_Y = 115  # y-position on belt (same as old code)


# # ==========================================
# # LOAD 50 IMAGES (25 def + 25 ok)
# # ==========================================
# def load_50_test_images():
#     def_files = list(TEST_DEF.glob("*.*"))
#     ok_files  = list(TEST_OK.glob("*.*"))

#     # Pick 25 randomly from each
#     def_sample = random.sample(def_files, 25)
#     ok_sample  = random.sample(ok_files, 25)

#     all_files = def_sample + ok_sample
#     random.shuffle(all_files)

#     images = []
#     for i, path in enumerate(all_files):
#         clean_img = Image.open(path).convert("RGB")       # clean image for prediction
#         belt_img  = clean_img.convert("RGBA").resize((PRODUCT_W, PRODUCT_H))

#         images.append({
#             "image_name": f"Image {i}",
#             "clean_img": clean_img,      # used for prediction
#             "belt_img": belt_img,        # used for animation
#             "path": path
#         })
#     return images


# # ==========================================
# # BELT FRAMES
# # ==========================================
# belt_frames = generate_belt_frames()
# BELT_COUNT = len(belt_frames)


# # ==========================================
# # DRAW BORDER + LABEL
# # ==========================================
# def add_border_and_label(frame, image_name, prediction, confidence, action):
#     img = frame.copy()
#     draw = ImageDraw.Draw(img)
#     w, h = img.size

#     # color
#     if prediction == "OK" and action == "ACCEPT":
#         color = (0, 220, 0)
#     elif prediction == "Defective" and action == "REJECT":
#         color = (220, 0, 0)
#     else:
#         color = (255, 215, 0)

#     # border
#     for i in range(6):
#         draw.rectangle([i, i, w-1-i, h-1-i], outline=color)

#     # info box
#     info = f"{image_name}\nPrediction: {prediction}\nConfidence: {confidence*100:.1f}%\nAction: {action}"
#     draw.rectangle([10, 10, 350, 110], fill=(0, 0, 0, 180))
#     draw.text((20, 20), info, fill=color)

#     return img


# # ==========================================
# # STREAMLIT UI
# # ==========================================
# st.set_page_config(
#     page_title="Agentic AI – Conveyor Defect Detection",
#     page_icon="🤖",
#     layout="wide",
# )

# st.markdown("<h1 style='text-align:center; color:#4CAF50;'>🏭 Agentic AI – Defect Detection on Conveyor Belt</h1>", unsafe_allow_html=True)
# st.markdown("<p style='text-align:center;'>Vision → Analysis → Decision → Report – Now automated on 50 images.</p>", unsafe_allow_html=True)

# st.markdown("---")

# left, right = st.columns([1.3, 1.7])

# with left:
#     st.subheader("🧪 Test Images (50)")
#     st.write("Randomly sampled: 25 Defective + 25 OK images, shuffled.")

#     test_images = load_50_test_images()

#     # thumbnails
#     thumb_cols = st.columns(5)
#     for i, item in enumerate(test_images[:10]):  # first 10 only
#         with thumb_cols[i % 5]:
#             st.image(item["clean_img"], caption=item["image_name"], width=100)

# with right:
#     st.subheader("🤖 Agent Pipeline")
#     st.markdown("""
#     **Agents used:**
#     - 👁️ Vision Agent – receives the product frame.
#     - 🧠 Analysis Agent – classifies using ResNet18 (clean image).
#     - ⚖️ Decision Agent – ACCEPT / REJECT.
#     - 📄 Report Agent – adds timestamp.
#     """)

# st.markdown("---")

# # animation area
# st.subheader("🎥 Live Detection on Conveyor Belt")
# image_placeholder = st.empty()
# results = []


# # ==========================================
# # RUN DETECTION ON 50 IMAGES
# # ==========================================
# if st.button("▶ Run Agentic Detection on 50 Images"):

#     for idx, item in enumerate(test_images):

#         # select belt frame
#         belt = belt_frames[idx % BELT_COUNT].copy()

#         # paste product image
#         bw, bh = belt.size
#         px = bw//2 - PRODUCT_W//2
#         belt.paste(item["belt_img"], (px, PRODUCT_Y), item["belt_img"])

#         # PASS CLEAN IMAGE TO AGENTS
#         state = run_agents_on_frame(
#             image_name=item["image_name"],
#             frame_id=idx,
#             frame=item["clean_img"]      # <------ CLEAN IMAGE !!!
#         )

#         prediction = state["prediction"]
#         confidence = state["confidence"]
#         action = state["action"]
#         timestamp = state["timestamp"]

#         # draw info / border
#         final_frame = add_border_and_label(
#             belt, item["image_name"], prediction, confidence, action
#         )

#         # show animation
#         image_placeholder.image(final_frame, use_container_width=True)
#         time.sleep(0.40)

#         # log summary
#         results.append({
#             "Image Name": item["image_name"],
#             "Frame Number": idx,
#             "Prediction": prediction,
#             "Confidence": round(confidence, 4),
#             "Action": action,
#             "Timestamp": timestamp
#         })

#     # ================================
#     # FINAL REPORT
#     # ================================
#     st.markdown("---")
#     st.subheader("📊 Final Inspection Report (50 Images)")

#     df = pd.DataFrame(results)
#     st.dataframe(df, use_container_width=True)

#     st.markdown(f"**Total images processed:** {len(df)}")
#     st.markdown(f"**✔ OK:** {(df['Prediction']=='OK').sum()}")
#     st.markdown(f"**❌ Defective:** {(df['Prediction']=='Defective').sum()}")
#     st.markdown(f"**⚠ Errors:** {(df['Prediction']=='ERROR').sum()}")

#     st.download_button(
#         "⬇ Download Inspection Report (CSV)",
#         df.to_csv(index=False),
#         "inspection_report_50_images.csv",
#         "text/csv"
#     )

# else:
#     st.info("Click **▶ Run Agentic Detection on 50 Images** to start the live demo.")




# import sys
# import random
# import time
# from pathlib import Path

# import streamlit as st
# import pandas as pd
# from PIL import Image, ImageDraw

# # Make src/ importable
# PROJECT_ROOT = Path(__file__).resolve().parent
# SRC_DIR = PROJECT_ROOT / "src"
# sys.path.append(str(SRC_DIR))

# from conveyor_belt import generate_belt_frames
# from agents_graph import run_agents_on_frame


# # ==========================================
# # CONFIG
# # ==========================================
# TEST_DEF = PROJECT_ROOT / "data" / "casting_data" / "test" / "def_front"
# TEST_OK  = PROJECT_ROOT / "data" / "casting_data" / "test" / "ok_front"

# PRODUCT_W = 90
# PRODUCT_H = 90
# PRODUCT_Y = 115


# # ==========================================
# # LOAD 50 IMAGES
# # ==========================================
# def load_50_test_images():
#     def_files = list(TEST_DEF.glob("*.*"))
#     ok_files  = list(TEST_OK.glob("*.*"))

#     def_sample = random.sample(def_files, 25)
#     ok_sample  = random.sample(ok_files, 25)

#     all_files = def_sample + ok_sample
#     random.shuffle(all_files)

#     images = []
#     for i, path in enumerate(all_files):
#         clean_img = Image.open(path).convert("RGB")
#         belt_img  = clean_img.convert("RGBA").resize((PRODUCT_W, PRODUCT_H))

#         images.append({
#             "image_name": f"Image {i}",
#             "clean_img": clean_img,
#             "belt_img": belt_img,
#             "path": path
#         })
#     return images


# # ==========================================
# # BELT FRAMES
# # ==========================================
# belt_frames = generate_belt_frames()
# BELT_COUNT = len(belt_frames)


# # ==========================================
# # DRAW BORDER + LABEL
# # ==========================================
# def add_border_and_label(frame, image_name, prediction, confidence, action):
#     img = frame.copy()
#     draw = ImageDraw.Draw(img)
#     w, h = img.size

#     if prediction == "OK" and action == "ACCEPT":
#         color = (0, 220, 0)
#     elif prediction == "Defective" and action == "REJECT":
#         color = (220, 0, 0)
#     else:
#         color = (255, 215, 0)

#     # border
#     for i in range(6):
#         draw.rectangle([i, i, w-1-i, h-1-i], outline=color)

#     info = f"{image_name}\nPrediction: {prediction}\nConfidence: {confidence*100:.1f}%\nAction: {action}"
#     draw.rectangle([10, 10, 350, 110], fill=(0, 0, 0, 160))
#     draw.text((20, 20), info, fill=color)

#     return img


# # ==========================================
# # STREAMLIT UI
# # ==========================================
# st.set_page_config(
#     page_title="Agentic AI – Conveyor Defect Detection",
#     page_icon="🤖",
#     layout="wide",
# )

# st.markdown("""
# <h1 style='text-align:center; color:#4CAF50;'>🏭 Agentic AI – Defect Detection on Conveyor Belt</h1>
# """, unsafe_allow_html=True)

# st.markdown("---")


# # ==========================================
# # LIVE DETECTION (TOP SECTION)
# # ==========================================
# st.subheader("🎥 Live Detection on Conveyor Belt")

# # GREEN PLAY BUTTON STYLE
# st.markdown("""
# <style>
# .play-btn {
#     background-color:#27ae60;
#     color:white;
#     padding:14px 35px;
#     border-radius:12px;
#     font-size:20px;
#     font-weight:bold;
#     border:none;
# }
# </style>
# """, unsafe_allow_html=True)

# start = st.button("▶ Start Detection (50 Images)", key="play", help="Start Conveyor", type="primary")

# image_placeholder = st.empty()
# results = []


# # ==========================================
# # RUN DETECTION
# # ==========================================
# if start:

#     test_images = load_50_test_images()
#     start_time = time.time()

#     for idx, item in enumerate(test_images):

#         belt = belt_frames[idx % BELT_COUNT].copy()
#         bw, bh = belt.size

#         px = bw//2 - PRODUCT_W//2
#         belt.paste(item["belt_img"], (px, PRODUCT_Y), item["belt_img"])

#         state = run_agents_on_frame(
#             image_name=item["image_name"],
#             frame_id=idx,
#             frame=item["clean_img"]
#         )

#         prediction = state["prediction"]
#         confidence = state["confidence"]
#         action = state["action"]
#         timestamp = state["timestamp"]

#         final_frame = add_border_and_label(
#             belt, item["image_name"], prediction, confidence, action
#         )

#         image_placeholder.image(final_frame, use_container_width=True)
#         time.sleep(0.40)

#         results.append({
#             "Image Name": item["image_name"],
#             "Frame Number": idx,
#             "Prediction": prediction,
#             "Confidence": round(confidence, 4),
#             "Action": action,
#             "Timestamp": timestamp
#         })

#     elapsed = time.time() - start_time
#     speed = round(50 / elapsed, 2)


#     # ==========================================
#     # SYSTEM STATUS SECTION
#     # ==========================================
#     st.markdown("---")
#     st.subheader("🛠️ System Status")

#     st.markdown("""
#     <style>
#     .status-box {
#         display: inline-block;
#         padding: 8px 18px;
#         margin-right: 14px;
#         background-color: #e8ffe8;
#         border-left: 8px solid #27ae60;
#         border-radius: 8px;
#         font-size: 16px;
#         font-weight: 600;
#     }
#     </style>
#     """, unsafe_allow_html=True)

#     st.markdown("""
#     <div class='status-box'>👁️ Vision Agent – Active</div>
#     <div class='status-box'>🧠 Analysis Agent – Active</div>
#     <div class='status-box'>⚖️ Decision Agent – Active</div>
#     <div class='status-box'>📄 Report Agent – Active</div>
#     """, unsafe_allow_html=True)


#     # ==========================================
#     # PRODUCTION STATUS SECTION
#     # ==========================================
#     st.markdown("---")
#     st.subheader("📦 Production Status")

#     df = pd.DataFrame(results)
#     ok_count = (df["Prediction"] == "OK").sum()
#     def_count = (df["Prediction"] == "Defective").sum()

#     col1, col2, col3, col4 = st.columns(4)
#     col1.metric("Total Processed", "50")
#     col2.metric("OK Items", ok_count)
#     col3.metric("Defective Items", def_count)
#     col4.metric("Speed (items/sec)", speed)


#     # ==========================================
#     # FINAL INSPECTION REPORT — Screenshot 250 Style
#     # ==========================================
#     st.markdown("---")
#     st.markdown("""
#     <h2 style='color:#333;'>📊 Final Inspection Report (50 Images)</h2>
#     """, unsafe_allow_html=True)

#     st.markdown("""
#     <style>
#     .report-container {
#         background: linear-gradient(to bottom, #e8f6ff, #ffffff);
#         padding: 25px;
#         border-radius: 12px;
#         margin-bottom: 20px;
#     }
#     table {
#         width: 100% !important;
#         border-collapse: separate;
#         border-spacing: 0;
#     }
#     th {
#         background-color: #d1f5d3 !important;
#         padding: 12px !important;
#         font-size: 16px !important;
#         color: #333 !important;
#     }
#     td {
#         padding: 10px !important;
#         font-size: 15px !important;
#     }
#     </style>
#     """, unsafe_allow_html=True)

#     # Badge styles
#     def badge_prediction(val):
#         if val == "OK":
#             return "background-color:#2ecc71; color:white; border-radius:14px; padding:5px 12px; text-align:center;"
#         else:
#             return "background-color:#e74c3c; color:white; border-radius:14px; padding:5px 12px; text-align:center;"

#     def badge_action(val):
#         if val == "ACCEPT":
#             return "background-color:#3498db; color:white; border-radius:14px; padding:5px 12px; text-align:center;"
#         else:
#             return "background-color:#f39c12; color:white; border-radius:14px; padding:5px 12px; text-align:center;"

#     df_style = df.copy()
#     df_style["Prediction"] = df_style["Prediction"].apply(lambda x: f"<span style='{badge_prediction(x)}'>{x}</span>")
#     df_style["Action"] = df_style["Action"].apply(lambda x: f"<span style='{badge_action(x)}'>{x}</span>")

#     st.markdown("<div class='report-container'>", unsafe_allow_html=True)
#     st.write(df_style.to_html(escape=False, index=False), unsafe_allow_html=True)
#     st.markdown("</div>", unsafe_allow_html=True)

#     st.download_button(
#         "⬇ Download Inspection Report (CSV)",
#         df.to_csv(index=False),
#         "inspection_report_50_images.csv",
#         "text/csv"
#     )

# else:
#     st.info("Click **▶ Start Detection (50 Images)** to begin simulation.")





# import sys
# import random
# import time
# from pathlib import Path

# import streamlit as st
# import pandas as pd
# from PIL import Image, ImageDraw

# # Make src/ importable
# PROJECT_ROOT = Path(__file__).resolve().parent
# SRC_DIR = PROJECT_ROOT / "src"
# sys.path.append(str(SRC_DIR))

# from conveyor_belt import generate_belt_frames
# from agents_graph import run_agents_on_frame


# # ==========================================
# # CONFIG
# # ==========================================
# TEST_DEF = PROJECT_ROOT / "data" / "casting_data" / "test" / "def_front"
# TEST_OK  = PROJECT_ROOT / "data" / "casting_data" / "test" / "ok_front"

# PRODUCT_W = 90
# PRODUCT_H = 90
# PRODUCT_Y = 115  # Y position on belt


# # ==========================================
# # LOAD 50 IMAGES
# # ==========================================
# def load_50_test_images():
#     def_files = list(TEST_DEF.glob("*.*"))
#     ok_files  = list(TEST_OK.glob("*.*"))

#     def_sample = random.sample(def_files, 25)
#     ok_sample  = random.sample(ok_files, 25)

#     all_files = def_sample + ok_sample
#     random.shuffle(all_files)

#     images = []
#     for i, path in enumerate(all_files):
#         clean_img = Image.open(path).convert("RGB")
#         belt_img  = clean_img.convert("RGBA").resize((PRODUCT_W, PRODUCT_H))

#         images.append({
#             "image_name": f"Image {i}",
#             "clean_img": clean_img,
#             "belt_img": belt_img,
#             "path": path
#         })
#     return images


# # ==========================================
# # BELT FRAMES (MOVING BELT)
# # ==========================================
# belt_frames = generate_belt_frames()
# BELT_COUNT = len(belt_frames)


# # ==========================================
# # DRAW BORDER + LABEL
# # ==========================================
# def add_border_and_label(frame, image_name, prediction, confidence, action):
#     img = frame.copy()
#     draw = ImageDraw.Draw(img)
#     w, h = img.size

#     if prediction == "OK" and action == "ACCEPT":
#         color = (0, 220, 0)
#     elif prediction == "Defective" and action == "REJECT":
#         color = (220, 0, 0)
#     else:
#         color = (255, 215, 0)

#     for i in range(6):
#         draw.rectangle([i, i, w-1-i, h-1-i], outline=color)

#     info = f"{image_name}\nPrediction: {prediction}\nConfidence: {confidence*100:.1f}%\nAction: {action}"
#     draw.rectangle([10, 10, 350, 110], fill=(0, 0, 0, 160))
#     draw.text((20, 20), info, fill=color)

#     return img


# # ==========================================
# # STREAMLIT UI
# # ==========================================
# st.set_page_config(
#     page_title="Agentic AI – Conveyor Defect Detection",
#     page_icon="🤖",
#     layout="wide",
# )

# st.markdown("""
# <h1 style='text-align:center; color:#4CAF50;'>🏭 Agentic AI – Defect Detection on Conveyor Belt</h1>
# """, unsafe_allow_html=True)

# st.markdown("---")


# # ==========================================
# # LIVE DETECTION SECTION
# # ==========================================
# st.subheader("🎥 Live Detection on Conveyor Belt")

# # Green play button
# start = st.button("▶ Start Detection (50 Images)", key="play")

# image_placeholder = st.empty()
# results = []


# # ==========================================
# # RUN DETECTION WITH FULL ANIMATION
# # ==========================================
# if start:

#     test_images = load_50_test_images()
#     start_time = time.time()

#     for idx, item in enumerate(test_images):

#         clean_img = item["clean_img"]
#         belt_img = item["belt_img"]

#         bw, bh = belt_frames[0].size
#         center_x = bw//2 - PRODUCT_W//2

#         # -------------------------------
#         # 1) PRODUCT ENTERS: LEFT → CENTER
#         # -------------------------------
#         for x in range(-PRODUCT_W, center_x, 25):
#             belt = belt_frames[x % BELT_COUNT].copy()
#             belt.paste(belt_img, (x, PRODUCT_Y), belt_img)
#             image_placeholder.image(belt, use_container_width=True)
#             time.sleep(0.03)

#         # -------------------------------
#         # 2) DETECTION AT CENTER
#         # -------------------------------
#         state = run_agents_on_frame(
#             image_name=item["image_name"],
#             frame_id=idx,
#             frame=clean_img
#         )

#         prediction = state["prediction"]
#         confidence = state["confidence"]
#         action = state["action"]
#         timestamp = state["timestamp"]

#         center_frame = belt_frames[idx % BELT_COUNT].copy()
#         center_frame.paste(belt_img, (center_x, PRODUCT_Y), belt_img)

#         detected_frame = add_border_and_label(
#             center_frame,
#             item["image_name"],
#             prediction,
#             confidence,
#             action
#         )

#         image_placeholder.image(detected_frame, use_container_width=True)
#         time.sleep(0.50)

#         # -------------------------------
#         # 3) PRODUCT EXITS: CENTER → RIGHT
#         # -------------------------------
#         for x in range(center_x, bw + PRODUCT_W, 25):
#             belt = belt_frames[x % BELT_COUNT].copy()
#             belt.paste(belt_img, (x, PRODUCT_Y), belt_img)
#             image_placeholder.image(belt, use_container_width=True)
#             time.sleep(0.03)

#         # Save result
#         results.append({
#             "Image Name": item["image_name"],
#             "Frame Number": idx,
#             "Prediction": prediction,
#             "Confidence": round(confidence, 4),
#             "Action": action,
#             "Timestamp": timestamp
#         })


#     elapsed = time.time() - start_time
#     speed = round(50 / elapsed, 2)


#     # ==========================================
#     # SYSTEM STATUS SECTION
#     # ==========================================
#     st.markdown("---")
#     st.subheader("🛠️ System Status")

#     st.markdown("""
#     <div style='padding:10px; background:#e8ffe8; border-left:10px solid #4CAF50; border-radius:8px; margin-bottom:5px;'>
#     👁️ Vision Agent – Active
#     </div>
#     <div style='padding:10px; background:#e8ffe8; border-left:10px solid #4CAF50; border-radius:8px; margin-bottom:5px;'>
#     🧠 Analysis Agent – Active
#     </div>
#     <div style='padding:10px; background:#e8ffe8; border-left:10px solid #4CAF50; border-radius:8px; margin-bottom:5px;'>
#     ⚖️ Decision Agent – Active
#     </div>
#     <div style='padding:10px; background:#e8ffe8; border-left:10px solid #4CAF50; border-radius:8px;'>
#     📄 Report Agent – Active
#     </div>
#     """, unsafe_allow_html=True)


#     # ==========================================
#     # PRODUCTION STATUS SECTION
#     # ==========================================
#     st.markdown("---")
#     st.subheader("📦 Production Status")

#     df = pd.DataFrame(results)
#     ok_count = (df["Prediction"] == "OK").sum()
#     def_count = (df["Prediction"] == "Defective").sum()

#     col1, col2, col3, col4 = st.columns(4)
#     col1.metric("Total Processed", "50")
#     col2.metric("OK Items", ok_count)
#     col3.metric("Defective Items", def_count)
#     col4.metric("Speed (items/sec)", speed)


#     # ==========================================
#     # FINAL INSPECTION REPORT – Styled Table
#     # ==========================================
#     st.markdown("---")
#     st.markdown("<h2>📊 Final Inspection Report (50 Images)</h2>", unsafe_allow_html=True)

#     # table styling
#     st.markdown("""
#     <style>
#     .report-container {
#         background: linear-gradient(to bottom, #e8f6ff, #ffffff);
#         padding: 25px;
#         border-radius: 12px;
#     }
#     th {
#         background:#d1f5d3 !important;
#         padding:12px;
#         font-size:16px;
#     }
#     td {
#         padding:10px;
#         font-size:15px;
#     }
#     </style>
#     """, unsafe_allow_html=True)

#     def badge_pred(v):
#         return f"<span style='background:#2ecc71;color:white;padding:5px 12px;border-radius:12px;'>{v}</span>" \
#                if v == "OK" else \
#                f"<span style='background:#e74c3c;color:white;padding:5px 12px;border-radius:12px;'>{v}</span>"

#     def badge_action(v):
#         return f"<span style='background:#3498db;color:white;padding:5px 12px;border-radius:12px;'>{v}</span>" \
#                if v == "ACCEPT" else \
#                f"<span style='background:#f39c12;color:white;padding:5px 12px;border-radius:12px;'>{v}</span>"

#     df2 = df.copy()
#     df2["Prediction"] = df2["Prediction"].apply(badge_pred)
#     df2["Action"] = df2["Action"].apply(badge_action)

#     st.markdown("<div class='report-container'>", unsafe_allow_html=True)
#     st.write(df2.to_html(escape=False, index=False), unsafe_allow_html=True)
#     st.markdown("</div>", unsafe_allow_html=True)

#     st.download_button(
#         "⬇ Download Report (CSV)",
#         df.to_csv(index=False),
#         "inspection_report_50_images.csv",
#         "text/csv",
#     )


# else:
#     st.info("Click **▶ Start Detection (50 Images)** to begin simulation.")

# import sys
# import random
# import time
# from pathlib import Path

# import streamlit as st
# import pandas as pd
# from PIL import Image, ImageDraw

# # Make src/ importable
# PROJECT_ROOT = Path(__file__).resolve().parent
# SRC_DIR = PROJECT_ROOT / "src"
# sys.path.append(str(SRC_DIR))

# from conveyor_belt import generate_belt_frames
# from agents_graph import run_agents_on_frame


# # ==========================================
# # CONFIG
# # ==========================================
# TEST_DEF = PROJECT_ROOT / "data" / "casting_data" / "test" / "def_front"
# TEST_OK  = PROJECT_ROOT / "data" / "casting_data" / "test" / "ok_front"

# PRODUCT_W = 90
# PRODUCT_H = 90
# PRODUCT_Y = 115  # Y position on belt


# # ==========================================
# # LOAD 50 IMAGES
# # ==========================================
# def load_50_test_images():
#     def_files = list(TEST_DEF.glob("*.*"))
#     ok_files  = list(TEST_OK.glob("*.*"))

#     def_sample = random.sample(def_files, 25)
#     ok_sample  = random.sample(ok_files, 25)

#     all_files = def_sample + ok_sample
#     random.shuffle(all_files)

#     images = []
#     for i, path in enumerate(all_files):
#         clean_img = Image.open(path).convert("RGB")
#         belt_img  = clean_img.convert("RGBA").resize((PRODUCT_W, PRODUCT_H))

#         images.append({
#             "image_name": f"Image {i}",
#             "clean_img": clean_img,
#             "belt_img": belt_img,
#             "path": path
#         })
#     return images


# # ==========================================
# # BELT FRAMES (MOVING BELT)
# # ==========================================
# belt_frames = generate_belt_frames()
# BELT_COUNT = len(belt_frames)


# # ==========================================
# # DRAW BORDER ONLY AROUND PRODUCT + LABEL
# # ==========================================
# def add_border_and_label(frame, px, py, pw, ph,
#                          image_name, prediction, confidence, action):
#     """
#     frame : PIL.Image belt frame with product pasted
#     px, py: top-left of product
#     pw, ph: width/height of product
#     """
#     img = frame.copy()
#     draw = ImageDraw.Draw(img)

#     # Decide color
#     if prediction == "OK" and action == "ACCEPT":
#         color = (0, 220, 0)      # green
#     elif prediction == "Defective" and action == "REJECT":
#         color = (220, 0, 0)      # red
#     else:
#         color = (255, 215, 0)    # yellow

#     # Border ONLY around the product tile
#     thickness = 4
#     for i in range(thickness):
#         draw.rectangle(
#             [px - i, py - i, px + pw + i, py + ph + i],
#             outline=color
#         )

#     # Info box in top-left corner
#     info = (
#         f"{image_name}\n"
#         f"Prediction: {prediction}\n"
#         f"Confidence: {confidence*100:.1f}%\n"
#         f"Action: {action}"
#     )
#     draw.rectangle([10, 10, 350, 110], fill=(0, 0, 0, 160))
#     draw.text((20, 20), info, fill=color)

#     return img


# # ==========================================
# # STREAMLIT UI
# # ==========================================
# st.set_page_config(
#     page_title="Agentic AI – Conveyor Defect Detection",
#     page_icon="🤖",
#     layout="wide",
# )

# st.markdown("""
# <h1 style='text-align:center; color:#4CAF50;'>🏭 Agentic AI – Defect Detection on Conveyor Belt</h1>
# """, unsafe_allow_html=True)

# st.markdown("---")


# # ==========================================
# # LIVE DETECTION SECTION
# # ==========================================
# st.subheader("🎥 Live Detection on Conveyor Belt")

# start = st.button("▶ Start Detection (50 Images)", key="play")

# image_placeholder = st.empty()
# results = []


# # ==========================================
# # RUN DETECTION WITH FULL ANIMATION
# # ==========================================
# if start:

#     test_images = load_50_test_images()
#     start_time = time.time()

#     for idx, item in enumerate(test_images):

#         clean_img = item["clean_img"]
#         belt_img = item["belt_img"]

#         bw, bh = belt_frames[0].size
#         center_x = bw // 2 - PRODUCT_W // 2

#         # -------------------------------
#         # 1) PRODUCT ENTERS: LEFT → CENTER
#         # -------------------------------
#         for x in range(-PRODUCT_W, center_x, 25):
#             belt = belt_frames[x % BELT_COUNT].copy()
#             belt.paste(belt_img, (x, PRODUCT_Y), belt_img)
#             image_placeholder.image(belt, use_container_width=True)
#             time.sleep(0.03)

#         # -------------------------------
#         # 2) DETECTION AT CENTER
#         # -------------------------------
#         state = run_agents_on_frame(
#             image_name=item["image_name"],
#             frame_id=idx,
#             frame=clean_img
#         )

#         prediction = state["prediction"]
#         confidence = state["confidence"]
#         action = state["action"]
#         timestamp = state["timestamp"]

#         center_frame = belt_frames[idx % BELT_COUNT].copy()
#         center_frame.paste(belt_img, (center_x, PRODUCT_Y), belt_img)

#         # highlight ONLY the product
#         detected_frame = add_border_and_label(
#             center_frame,
#             center_x, PRODUCT_Y, PRODUCT_W, PRODUCT_H,
#             item["image_name"],
#             prediction,
#             confidence,
#             action
#         )

#         image_placeholder.image(detected_frame, use_container_width=True)
#         time.sleep(0.50)

#         # -------------------------------
#         # 3) PRODUCT EXITS: CENTER → RIGHT
#         # -------------------------------
#         for x in range(center_x, bw + PRODUCT_W, 25):
#             belt = belt_frames[x % BELT_COUNT].copy()
#             belt.paste(belt_img, (x, PRODUCT_Y), belt_img)
#             image_placeholder.image(belt, use_container_width=True)
#             time.sleep(0.03)

#         # Save result
#         results.append({
#             "Image Name": item["image_name"],
#             "Frame Number": idx,
#             "Prediction": prediction,
#             "Confidence": round(confidence, 4),
#             "Action": action,
#             "Timestamp": timestamp
#         })

#     elapsed = time.time() - start_time
#     speed = round(50 / elapsed, 2)

#     # ==========================================
#     # SYSTEM STATUS SECTION
#     # ==========================================
#     st.markdown("---")
#     st.subheader("🛠️ System Status")

#     st.markdown("""
#     <div style='padding:10px; background:#e8ffe8; border-left:10px solid #4CAF50; border-radius:8px; margin-bottom:5px;'>
#     👁️ Vision Agent – Active
#     </div>
#     <div style='padding:10px; background:#e8ffe8; border-left:10px solid #4CAF50; border-radius:8px; margin-bottom:5px;'>
#     🧠 Analysis Agent – Active
#     </div>
#     <div style='padding:10px; background:#e8ffe8; border-left:10px solid #4CAF50; border-radius:8px; margin-bottom:5px;'>
#     ⚖️ Decision Agent – Active
#     </div>
#     <div style='padding:10px; background:#e8ffe8; border-left:10px solid #4CAF50; border-radius:8px;'>
#     📄 Report Agent – Active
#     </div>
#     """, unsafe_allow_html=True)

#     # ==========================================
#     # PRODUCTION STATUS SECTION
#     # ==========================================
#     st.markdown("---")
#     st.subheader("📦 Production Status")

#     df = pd.DataFrame(results)
#     ok_count = (df["Prediction"] == "OK").sum()
#     def_count = (df["Prediction"] == "Defective").sum()

#     col1, col2, col3, col4 = st.columns(4)
#     col1.metric("Total Processed", "50")
#     col2.metric("OK Items", ok_count)
#     col3.metric("Defective Items", def_count)
#     col4.metric("Speed (items/sec)", speed)

#     # ==========================================
#     # FINAL INSPECTION REPORT – Styled Table
#     # ==========================================
#     st.markdown("---")
#     st.markdown("<h2>📊 Final Inspection Report (50 Images)</h2>", unsafe_allow_html=True)

#     st.markdown("""
#     <style>
#     .report-container {
#         background: linear-gradient(to bottom, #e8f6ff, #ffffff);
#         padding: 25px;
#         border-radius: 12px;
#     }
#     th {
#         background:#d1f5d3 !important;
#         padding:12px;
#         font-size:16px;
#     }
#     td {
#         padding:10px;
#         font-size:15px;
#     }
#     </style>
#     """, unsafe_allow_html=True)

#     def badge_pred(v):
#         return (
#             f"<span style='background:#2ecc71;color:white;padding:5px 12px;border-radius:12px;'>{v}</span>"
#             if v == "OK" else
#             f"<span style='background:#e74c3c;color:white;padding:5px 12px;border-radius:12px;'>{v}</span>"
#         )

#     def badge_action(v):
#         return (
#             f"<span style='background:#3498db;color:white;padding:5px 12px;border-radius:12px;'>{v}</span>"
#             if v == "ACCEPT" else
#             f"<span style='background:#f39c12;color:white;padding:5px 12px;border-radius:12px;'>{v}</span>"
#         )

#     df2 = df.copy()
#     df2["Prediction"] = df2["Prediction"].apply(badge_pred)
#     df2["Action"] = df2["Action"].apply(badge_action)

#     st.markdown("<div class='report-container'>", unsafe_allow_html=True)
#     st.write(df2.to_html(escape=False, index=False), unsafe_allow_html=True)
#     st.markdown("</div>", unsafe_allow_html=True)

#     st.download_button(
#         "⬇ Download Report (CSV)",
#         df.to_csv(index=False),
#         "inspection_report_50_images.csv",
#         "text/csv",
#     )

# else:
#     st.info("Click **▶ Start Detection (50 Images)** to begin simulation.")


# import sys
# import random
# import time
# from pathlib import Path

# import streamlit as st
# import pandas as pd
# from PIL import Image, ImageDraw

# # Make src/ importable
# PROJECT_ROOT = Path(__file__).resolve().parent
# SRC_DIR = PROJECT_ROOT / "src"
# sys.path.append(str(SRC_DIR))

# from conveyor_belt import generate_belt_frames
# from agents_graph import run_agents_on_frame


# # ==========================================
# # CONFIG
# # ==========================================
# TEST_DEF = PROJECT_ROOT / "data" / "casting_data" / "test" / "def_front"
# TEST_OK  = PROJECT_ROOT / "data" / "casting_data" / "test" / "ok_front"

# PRODUCT_W = 90
# PRODUCT_H = 90
# PRODUCT_Y = 115


# # ==========================================
# # LOAD 50 IMAGES
# # ==========================================
# def load_50_test_images():
#     def_files = list(TEST_DEF.glob("*.*"))
#     ok_files  = list(TEST_OK.glob("*.*"))

#     def_sample = random.sample(def_files, 25)
#     ok_sample  = random.sample(ok_files, 25)

#     all_files = def_sample + ok_sample
#     random.shuffle(all_files)

#     images = []
#     for i, path in enumerate(all_files):
#         clean_img = Image.open(path).convert("RGB")
#         belt_img  = clean_img.convert("RGBA").resize((PRODUCT_W, PRODUCT_H))

#         images.append({
#             "image_name": f"Image {i}",
#             "clean_img": clean_img,
#             "belt_img": belt_img,
#             "path": path
#         })
#     return images


# # ==========================================
# # BELT FRAMES
# # ==========================================
# belt_frames = generate_belt_frames()
# BELT_COUNT = len(belt_frames)


# # ==========================================
# # BORDER + LABEL
# # ==========================================
# def add_border_and_label(frame, px, py, pw, ph,
#                          image_name, prediction, confidence, action):

#     img = frame.copy()
#     draw = ImageDraw.Draw(img)

#     # Border color
#     if prediction == "OK" and action == "ACCEPT":
#         color = (0, 220, 0)
#     elif prediction == "Defective" and action == "REJECT":
#         color = (220, 0, 0)
#     else:
#         color = (255, 215, 0)

#     for i in range(4):
#         draw.rectangle(
#             [px - i, py - i, px + pw + i, py + ph + i],
#             outline=color
#         )

#     info = (
#         f"{image_name}\n"
#         f"Prediction: {prediction}\n"
#         f"Confidence: {confidence*100:.1f}%\n"
#         f"Action: {action}"
#     )
#     draw.rectangle([10, 10, 350, 115], fill=(0, 0, 0, 160))
#     draw.text((20, 20), info, fill=color)

#     return img


# # ==========================================
# # STREAMLIT SETUP
# # ==========================================
# st.set_page_config(
#     page_title="Agentic AI – Conveyor Defect Detection",
#     page_icon="🤖",
#     layout="wide",
# )

# st.markdown("""
# <style>
# .block-container { max-width: 1400px; }
# .report-container table { width: 100% !important; }
# </style>
# """, unsafe_allow_html=True)

# st.markdown("""
# <h1 style='text-align:center; color:#4CAF50;'>🏭 Agentic AI – Defect Detection on Conveyor Belt</h1>
# """, unsafe_allow_html=True)

# st.markdown("---")


# # ==========================================
# # LIVE DETECTION
# # ==========================================
# st.subheader("🎥 Live Detection on Conveyor Belt")
# start = st.button("▶ Play Agentic Demo (50 Images)", key="play")

# image_placeholder = st.empty()
# results = []


# # ==========================================
# # MAIN DETECTION LOOP
# # ==========================================
# if start:

#     test_images = load_50_test_images()
#     start_time = time.time()

#     for idx, item in enumerate(test_images):

#         clean_img = item["clean_img"]
#         belt_img = item["belt_img"]

#         bw, bh = belt_frames[0].size
#         center_x = bw // 2 - PRODUCT_W // 2

#         # product enters
#         for x in range(-PRODUCT_W, center_x, 15):
#             belt = belt_frames[x % BELT_COUNT].copy()
#             belt.paste(belt_img, (x, PRODUCT_Y), belt_img)
#             image_placeholder.image(belt, use_container_width=True)
#             time.sleep(0.06)

#         # run agentic workflow
#         state = run_agents_on_frame(
#             image_name=item["image_name"],
#             frame_id=idx,
#             frame=clean_img
#         )

#         prediction = state["prediction"]
#         confidence = state["confidence"]
#         action = state["action"]
#         timestamp = state["timestamp"]

#         frame_center = belt_frames[idx % BELT_COUNT].copy()
#         frame_center.paste(belt_img, (center_x, PRODUCT_Y), belt_img)

#         detected = add_border_and_label(
#             frame_center,
#             center_x, PRODUCT_Y, PRODUCT_W, PRODUCT_H,
#             item["image_name"],
#             prediction,
#             confidence,
#             action
#         )

#         image_placeholder.image(detected, use_container_width=True)
#         time.sleep(0.7)

#         # exit
#         for x in range(center_x, bw + PRODUCT_W, 15):
#             belt = belt_frames[x % BELT_COUNT].copy()
#             belt.paste(belt_img, (x, PRODUCT_Y), belt_img)
#             image_placeholder.image(belt, use_container_width=True)
#             time.sleep(0.06)

#         results.append({
#             "Image Name": item["image_name"],
#             "Frame Number": idx,
#             "Prediction": prediction,
#             "Confidence": round(confidence, 4),
#             "Action": action,
#             "Timestamp": timestamp
#         })

#     # final metrics
#     elapsed = time.time() - start_time
#     speed = round(50 / elapsed, 2)

#     df = pd.DataFrame(results)

#     # ==========================================
#     # PRODUCTION STATUS
#     # ==========================================
#     st.markdown("<h2>📦 Production Status</h2>", unsafe_allow_html=True)

#     ok_count = (df["Prediction"] == "OK").sum()
#     def_count = (df["Prediction"] == "Defective").sum()

#     col1, col2, col3, col4 = st.columns(4)
#     col1.metric("Total Processed", "50")
#     col2.metric("OK Items", ok_count)
#     col3.metric("Defective Items", def_count)
#     col4.metric("Speed (items/sec)", speed)

#     # ==========================================
#     # FINAL REPORT
#     # ==========================================
#     st.markdown("---")
#     st.markdown("<h2>📊 Final Inspection Report (50 Images)</h2>", unsafe_allow_html=True)

#     st.markdown("""
#     <style>
#     .report-container {
#         background: linear-gradient(to bottom, #e8f6ff, #ffffff);
#         padding: 25px;
#         border-radius: 12px;
#     }
#     th { background:#d1f5d3 !important; padding:12px; }
#     td { padding:10px; }
#     </style>
#     """, unsafe_allow_html=True)

#     def badge_pred(v):
#         return (f"<span style='background:#2ecc71;color:white;padding:6px 12px;border-radius:12px;'>{v}</span>"
#                 if v == "OK" else
#                 f"<span style='background:#e74c3c;color:white;padding:6px 12px;border-radius:12px;'>{v}</span>")

#     def badge_action(v):
#         return (f"<span style='background:#3498db;color:white;padding:6px 12px;border-radius:12px;'>{v}</span>"
#                 if v == "ACCEPT" else
#                 f"<span style='background:#f39c12;color:white;padding:6px 12px;border-radius:12px;'>{v}</span>")

#     df2 = df.copy()
#     df2["Prediction"] = df2["Prediction"].apply(badge_pred)
#     df2["Action"] = df2["Action"].apply(badge_action)

#     st.markdown("<div class='report-container'>", unsafe_allow_html=True)
#     st.write(df2.to_html(escape=False, index=False), unsafe_allow_html=True)
#     st.markdown("</div>", unsafe_allow_html=True)

#     st.download_button(
#         "⬇ Download Report (CSV)",
#         df.to_csv(index=False),
#         "inspection_report_50_images.csv",
#         "text/csv",
#     )

# else:
#     st.info("Click **▶ Play Agentic Demo (50 Images)** to begin simulation.")




# import sys
# import random
# import time
# from pathlib import Path

# import streamlit as st
# import pandas as pd
# from PIL import Image, ImageDraw

# # Make src/ importable
# PROJECT_ROOT = Path(__file__).resolve().parent
# SRC_DIR = PROJECT_ROOT / "src"
# sys.path.append(str(SRC_DIR))

# from conveyor_belt import generate_belt_frames
# from agents_graph import run_agents_on_frame


# # ==========================================
# # CONFIG
# # ==========================================
# TEST_DEF = PROJECT_ROOT / "data" / "casting_data" / "test" / "def_front"
# TEST_OK  = PROJECT_ROOT / "data" / "casting_data" / "test" / "ok_front"

# PRODUCT_W = 90
# PRODUCT_H = 90
# PRODUCT_Y = 115


# # ==========================================
# # LOAD 50 IMAGES
# # ==========================================
# def load_50_test_images():
#     def_files = list(TEST_DEF.glob("*.*"))
#     ok_files  = list(TEST_OK.glob("*.*"))

#     def_sample = random.sample(def_files, 25)
#     ok_sample  = random.sample(ok_files, 25)

#     all_files = def_sample + ok_sample
#     random.shuffle(all_files)

#     images = []
#     for i, path in enumerate(all_files):
#         clean_img = Image.open(path).convert("RGB")
#         belt_img  = clean_img.convert("RGBA").resize((PRODUCT_W, PRODUCT_H))

#         images.append({
#             "image_name": f"Image {i}",
#             "clean_img": clean_img,
#             "belt_img": belt_img,
#             "path": path
#         })
#     return images


# # ==========================================
# # BELT FRAMES
# # ==========================================
# belt_frames = generate_belt_frames()
# BELT_COUNT = len(belt_frames)


# # ==========================================
# # BORDER + LABEL
# # ==========================================
# def add_border_and_label(frame, px, py, pw, ph,
#                          image_name, prediction, confidence, action):

#     img = frame.copy()
#     draw = ImageDraw.Draw(img)

#     if prediction == "OK" and action == "ACCEPT":
#         color = (0, 220, 0)
#     elif prediction == "Defective" and action == "REJECT":
#         color = (220, 0, 0)
#     else:
#         color = (255, 215, 0)

#     for i in range(4):
#         draw.rectangle(
#             [px - i, py - i, px + pw + i, py + ph + i],
#             outline=color
#         )

#     info = (
#         f"{image_name}\n"
#         f"Prediction: {prediction}\n"
#         f"Confidence: {confidence*100:.1f}%\n"
#         f"Action: {action}"
#     )

#     draw.rectangle([10, 10, 350, 115], fill=(0, 0, 0, 160))
#     draw.text((20, 20), info, fill=color)

#     return img


# # ==========================================
# # STREAMLIT SETUP
# # ==========================================
# st.set_page_config(
#     page_title="Agentic AI – Conveyor Defect Detection",
#     page_icon="🤖",
#     layout="wide",
# )

# st.markdown("""
# <style>
# .block-container { max-width: 1400px; }
# </style>
# """, unsafe_allow_html=True)

# st.markdown("<h1 style='text-align:center; color:#4CAF50;'>🏭 Agentic AI – Defect Detection on Conveyor Belt</h1>", unsafe_allow_html=True)
# st.markdown("---")


# # ==========================================
# # LIVE DETECTION
# # ==========================================
# st.subheader("🎥 Live Detection on Conveyor Belt")
# start = st.button("▶ Play Agentic Demo ", key="play")

# image_placeholder = st.empty()
# results = []


# # ==========================================
# # MAIN DETECTION LOOP
# # ==========================================
# if start:

#     test_images = load_50_test_images()
#     start_time = time.time()

#     for idx, item in enumerate(test_images):

#         clean_img = item["clean_img"]
#         belt_img = item["belt_img"]

#         bw, bh = belt_frames[0].size
#         center_x = bw // 2 - PRODUCT_W // 2

#         # product enters
#         for x in range(-PRODUCT_W, center_x, 15):
#             belt = belt_frames[x % BELT_COUNT].copy()
#             belt.paste(belt_img, (x, PRODUCT_Y), belt_img)
#             image_placeholder.image(belt, use_container_width=True)
#             time.sleep(0.06)

#         # run agent workflow
#         state = run_agents_on_frame(
#             image_name=item["image_name"],
#             frame_id=idx,
#             frame=clean_img
#         )

#         prediction = state["prediction"]
#         confidence = state["confidence"]
#         action = state["action"]
#         timestamp = state["timestamp"]

#         frame_center = belt_frames[idx % BELT_COUNT].copy()
#         frame_center.paste(belt_img, (center_x, PRODUCT_Y), belt_img)

#         detected = add_border_and_label(
#             frame_center,
#             center_x, PRODUCT_Y, PRODUCT_W, PRODUCT_H,
#             item["image_name"],
#             prediction,
#             confidence,
#             action
#         )

#         image_placeholder.image(detected, use_container_width=True)
#         time.sleep(0.7)

#         # exit
#         for x in range(center_x, bw + PRODUCT_W, 15):
#             belt = belt_frames[x % BELT_COUNT].copy()
#             belt.paste(belt_img, (x, PRODUCT_Y), belt_img)
#             image_placeholder.image(belt, use_container_width=True)
#             time.sleep(0.06)

#         results.append({
#             "Image Name": item["image_name"],
#             "Frame Number": idx,
#             "Prediction": prediction,
#             "Confidence": round(confidence, 4),
#             "Action": action,
#             "Timestamp": timestamp
#         })

#     # time calculations
#     elapsed = time.time() - start_time
#     speed = round(50 / elapsed, 2)

#     df = pd.DataFrame(results)


#     # ==========================================
#     # PRODUCTION STATUS
#     # ==========================================
#     st.markdown("<h2>📦 Production Status</h2>", unsafe_allow_html=True)

#     ok_count = (df["Prediction"] == "OK").sum()
#     def_count = (df["Prediction"] == "Defective").sum()

#     col1, col2, col3, col4 = st.columns(4)
#     col1.metric("Total Processed", "50")
#     col2.metric("OK Items", ok_count)
#     col3.metric("Defective Items", def_count)
#     col4.metric("Speed (items/sec)", speed)


#     # ==========================================
#     # FINAL REPORT (UPDATED FULL WIDTH)
#     # ==========================================
#     st.markdown("---")
#     st.markdown("<h2>📊 Final Inspection Report</h2>", unsafe_allow_html=True)

#     st.markdown("""
#     <style>
#     .report-container {
#         background: linear-gradient(to bottom, #e8f6ff, #ffffff);
#         padding: 25px;
#         border-radius: 12px;
#         width: 100% !important;           /* FULL WIDTH */
#     }
#     .report-container table {
#         width: 100% !important;           /* FULL WIDTH */
#         table-layout: fixed;              /* EVEN COLUMNS */
#     }
#     th {
#         background:#d1f5d3 !important;
#         padding:12px;
#         font-weight:700;
#     }
#     td {
#         padding:10px;
#     }
#     </style>
#     """, unsafe_allow_html=True)

#     def badge_pred(v):
#         return (f"<span style='background:#2ecc71;color:white;padding:6px 12px;border-radius:12px;'>{v}</span>"
#                 if v == "OK" else
#                 f"<span style='background:#e74c3c;color:white;padding:6px 12px;border-radius:12px;'>{v}</span>")

#     def badge_action(v):
#         return (f"<span style='background:#3498db;color:white;padding:6px 12px;border-radius:12px;'>{v}</span>"
#                 if v == "ACCEPT" else
#                 f"<span style='background:#f39c12;color:white;padding:6px 12px;border-radius:12px;'>{v}</span>")

#     df2 = df.copy()
#     df2["Prediction"] = df2["Prediction"].apply(badge_pred)
#     df2["Action"] = df2["Action"].apply(badge_action)

#     st.markdown("<div class='report-container'>", unsafe_allow_html=True)
#     st.write(df2.to_html(escape=False, index=False), unsafe_allow_html=True)
#     st.markdown("</div>", unsafe_allow_html=True)

#     st.download_button(
#         "⬇ Download Report (CSV)",
#         df.to_csv(index=False),
#         "inspection_report_50_images.csv",
#         "text/csv",
#     )

# else:
#     st.info("Click **▶ Play Agentic Demo** to begin simulation.")

##### current code*********
# import sys
# import random
# import time
# from pathlib import Path

# import streamlit as st
# import pandas as pd
# from PIL import Image, ImageDraw

# # Make src/ importable
# PROJECT_ROOT = Path(__file__).resolve().parent
# SRC_DIR = PROJECT_ROOT / "src"
# sys.path.append(str(SRC_DIR))

# from conveyor_belt import generate_belt_frames
# from agents_graph import run_agents_on_frame


# # ==========================================
# # CONFIG
# # ==========================================
# TEST_DEF = PROJECT_ROOT / "data" / "casting_data" / "test" / "def_front"
# TEST_OK  = PROJECT_ROOT / "data" / "casting_data" / "test" / "ok_front"

# PRODUCT_W = 90
# PRODUCT_H = 90
# PRODUCT_Y = 115


# # ==========================================
# # RANDOM REALISTIC BATCH 30–80 TOTAL ITEMS
# # ==========================================
# def load_random_batch():
#     def_files = list(TEST_DEF.glob("*.*"))
#     ok_files  = list(TEST_OK.glob("*.*"))

#     total_def = len(def_files)
#     total_ok  = len(ok_files)

#     total_all = total_def + total_ok
#     if total_all == 0:
#         return []

#     p_def = total_def / total_all
#     p_ok  = total_ok  / total_all

#     # RANDOM batch size: changes every run
#     BATCH_SIZE = random.randint(30, 80)

#     num_def = int(BATCH_SIZE * p_def)
#     num_ok  = BATCH_SIZE - num_def

#     def_sample = random.sample(def_files, min(num_def, total_def))
#     ok_sample  = random.sample(ok_files, min(num_ok, total_ok))

#     all_files = def_sample + ok_sample
#     random.shuffle(all_files)

#     images = []
#     for i, path in enumerate(all_files):
#         clean_img = Image.open(path).convert("RGB")
#         belt_img  = clean_img.convert("RGBA").resize((PRODUCT_W, PRODUCT_H))

#         images.append({
#             "image_name": f"Image {i}",
#             "clean_img": clean_img,
#             "belt_img": belt_img,
#         })
#     return images


# # ==========================================
# # BELT FRAMES
# # ==========================================
# belt_frames = generate_belt_frames()
# BELT_COUNT = len(belt_frames)


# # ==========================================
# # BORDER + LABEL
# # ==========================================
# def add_border_and_label(frame, px, py, pw, ph,
#                          image_name, prediction, confidence, action):

#     img = frame.copy()
#     draw = ImageDraw.Draw(img)

#     if prediction == "OK" and action == "ACCEPT":
#         color = (0, 220, 0)
#     elif prediction == "Defective" and action == "REJECT":
#         color = (220, 0, 0)
#     else:
#         color = (255, 215, 0)

#     for i in range(4):
#         draw.rectangle(
#             [px - i, py - i, px + pw + i, py + ph + i],
#             outline=color
#         )

#     info = (
#         f"{image_name}\n"
#         f"Prediction: {prediction}\n"
#         f"Confidence: {confidence*100:.1f}%\n"
#         f"Action: {action}"
#     )

#     draw.rectangle([10, 10, 350, 115], fill=(0, 0, 0, 160))
#     draw.text((20, 20), info, fill=color)

#     return img


# # ==========================================
# # STREAMLIT SETUP
# # ==========================================
# st.set_page_config(
#     page_title="Agentic AI – Conveyor Defect Detection",
#     page_icon="🤖",
#     layout="wide",
# )

# st.markdown("""
# <style>
# .block-container { max-width: 1400px; }

# .status-card {
#     padding: 16px;
#     background: #ffffff;
#     border-radius: 12px;
#     box-shadow: 0 3px 8px rgba(0,0,0,0.08);
#     margin-bottom: 18px;
#     border: 1px solid #ececec;
# }

# .status-title {
#     font-size: 1rem;
#     font-weight: 700;
#     margin-bottom: 6px;
#     color: #1a1a1a;
# }

# .status-value {
#     font-size: 1.4rem;
#     font-weight: 800;
#     color: #111827;
# }

# .status-sub {
#     font-size: 0.8rem;
#     color: #555;
# }
# </style>
# """, unsafe_allow_html=True)

# st.markdown("<h1 style='text-align:center; color:#4CAF50;'>🏭 Agentic AI – Defect Detection on Conveyor Belt</h1>", unsafe_allow_html=True)
# st.markdown("---")


# # ==========================================
# # LIVE DETECTION
# # ==========================================
# st.subheader("🎥 Live Detection on Conveyor Belt")
# start = st.button("▶ Start Batch Scan", key="play")

# image_placeholder = st.empty()
# results = []


# # ==========================================
# # MAIN DETECTION LOOP
# # ==========================================
# if start:

#     test_images = load_random_batch()
#     batch_size = len(test_images)

#     start_time = time.time()

#     for idx, item in enumerate(test_images):

#         clean_img = item["clean_img"]
#         belt_img = item["belt_img"]

#         bw, bh = belt_frames[0].size
#         center_x = bw // 2 - PRODUCT_W // 2

#         # entering
#         for x in range(-PRODUCT_W, center_x, 15):
#             belt = belt_frames[x % BELT_COUNT].copy()
#             belt.paste(belt_img, (x, PRODUCT_Y), belt_img)
#             image_placeholder.image(belt, use_container_width=True)
#             time.sleep(0.05)

#         # run agent workflow
#         state = run_agents_on_frame(
#             image_name=item["image_name"],
#             frame_id=idx,
#             frame=clean_img
#         )

#         prediction = state["prediction"]
#         confidence = state["confidence"]
#         action = state["action"]
#         timestamp = state["timestamp"]

#         frame_center = belt_frames[idx % BELT_COUNT].copy()
#         frame_center.paste(belt_img, (center_x, PRODUCT_Y), belt_img)

#         detected = add_border_and_label(
#             frame_center,
#             center_x, PRODUCT_Y, PRODUCT_W, PRODUCT_H,
#             item["image_name"],
#             prediction,
#             confidence,
#             action
#         )

#         image_placeholder.image(detected, use_container_width=True)
#         time.sleep(0.6)

#         # exit
#         for x in range(center_x, bw + PRODUCT_W, 15):
#             belt = belt_frames[x % BELT_COUNT].copy()
#             belt.paste(belt_img, (x, PRODUCT_Y), belt_img)
#             image_placeholder.image(belt, use_container_width=True)
#             time.sleep(0.05)

#         results.append({
#             "Image Name": item["image_name"],
#             "Frame Number": idx,
#             "Prediction": prediction,
#             "Confidence": round(confidence, 4),
#             "Action": action,
#             "Timestamp": timestamp
#         })

#     elapsed = time.time() - start_time
#     speed = round(batch_size / elapsed, 2)

#     df = pd.DataFrame(results)


#     # ==========================================
#     # PRODUCTION STATUS
#     # ==========================================
#     st.markdown(f"<h2>📦 Production Status (Batch Size: {batch_size})</h2>", unsafe_allow_html=True)

#     ok_count = (df["Prediction"] == "OK").sum()
#     def_count = (df["Prediction"] == "Defective").sum()

#     col1, col2, col3, col4 = st.columns(4)
#     col1.metric("Total Processed", batch_size)
#     col2.metric("OK Items", ok_count)
#     col3.metric("Defective Items", def_count)
#     col4.metric("Speed (items/sec)", speed)


#     # ==========================================
#     # FINAL REPORT + SYSTEM STATUS SIDE PANEL
#     # ==========================================
#     st.markdown("---")
#     st.markdown("<h2>📊 Final Inspection Report</h2>", unsafe_allow_html=True)

#     left, right = st.columns([2.2, 1])

#     # ---------------- LEFT (TABLE)
#     with left:
#         st.markdown("""
#         <style>
#         .report-container {
#             background: #f4fbff;
#             padding: 20px;
#             border-radius: 12px;
#             border: 1px solid #e1e5ea;
#         }
#         </style>
#         """, unsafe_allow_html=True)

#         df2 = df.copy()

#         def badge_pred(v):
#             return (f"<span style='background:#2ecc71;color:white;padding:6px 12px;border-radius:12px;'>{v}</span>"
#                     if v == "OK" else
#                     f"<span style='background:#e74c3c;color:white;padding:6px 12px;border-radius:12px;'>{v}</span>")

#         def badge_action(v):
#             return (f"<span style='background:#3498db;color:white;padding:6px 12px;border-radius:12px;'>{v}</span>"
#                     if v == "ACCEPT" else
#                     f"<span style='background:#f39c12;color:white;padding:6px 12px;border-radius:12px;'>{v}</span>")

#         df2["Prediction"] = df2["Prediction"].apply(badge_pred)
#         df2["Action"]      = df2["Action"].apply(badge_action)

#         st.markdown("<div class='report-container'>", unsafe_allow_html=True)
#         st.write(df2.to_html(escape=False, index=False), unsafe_allow_html=True)
#         st.markdown("</div>", unsafe_allow_html=True)

#     # ---------------- RIGHT (SYSTEM STATUS)
#     with right:

#         # System Health
#         ok_ratio = ok_count / batch_size
#         avg_conf = df["Confidence"].mean()

#         if ok_ratio >= 0.9 and avg_conf >= 0.97:
#             health = "🟢 Healthy"
#         elif ok_ratio >= 0.75:
#             health = "🟡 Warning"
#         else:
#             health = "🔴 Critical"

#         st.markdown(f"""
#         <div class="status-card">
#             <div class="status-title">🩺 System Health</div>
#             <div class="status-value">{health}</div>
#             <div class="status-sub">Based on output quality & confidence</div>
#         </div>
#         """, unsafe_allow_html=True)

#         # Model
#         st.markdown("""
#         <div class="status-card">
#             <div class="status-title">🤖 Model Used</div>
#             <div class="status-value">ResNet-18</div>
#             <div class="status-sub">Version: v1.0</div>
#         </div>
#         """, unsafe_allow_html=True)

#         # Time taken
#         st.markdown(f"""
#         <div class="status-card">
#             <div class="status-title">⏱️ Total Time</div>
#             <div class="status-value">{elapsed:.2f} sec</div>
#             <div class="status-sub">End-to-end processing</div>
#         </div>
#         """, unsafe_allow_html=True)

#         # High confidence
#         high = (df["Confidence"] >= 0.98).sum()
#         low  = (df["Confidence"] < 0.90).sum()

#         st.markdown(f"""
#         <div class="status-card">
#             <div class="status-title">📈 High Confidence</div>
#             <div class="status-value">{high}</div>
#             <div class="status-sub">Confidence ≥ 98%</div>
#         </div>

#         <div class="status-card">
#             <div class="status-title">📉 Low Confidence</div>
#             <div class="status-value">{low}</div>
#             <div class="status-sub">Confidence &lt; 90%</div>
#         </div>
#         """, unsafe_allow_html=True)

#         # Accuracy Chart (OK vs DEF)
#         st.markdown("<div class='status-card'>", unsafe_allow_html=True)
#         st.subheader("📊 Accuracy Breakdown")
#         st.bar_chart(df["Prediction"].value_counts())
#         st.markdown("</div>", unsafe_allow_html=True)

#     # Download
#     st.download_button(
#         "⬇ Download Report (CSV)",
#         df.to_csv(index=False),
#         "inspection_report_batch.csv",
#         "text/csv",
#     )

# else:
#     st.info("Click **▶ Start Batch Scan** to begin.")


# import sys
# import random
# import time
# from pathlib import Path

# import streamlit as st
# import pandas as pd
# from PIL import Image, ImageDraw

# # Make src/ importable
# PROJECT_ROOT = Path(__file__).resolve().parent
# SRC_DIR = PROJECT_ROOT / "src"
# sys.path.append(str(SRC_DIR))

# from conveyor_belt import generate_belt_frames
# from agents_graph import run_agents_on_frame


# # ==========================================
# # CONFIG
# # ==========================================
# TEST_DEF = PROJECT_ROOT / "data" / "casting_data" / "test" / "def_front"
# TEST_OK  = PROJECT_ROOT / "data" / "casting_data" / "test" / "ok_front"

# PRODUCT_W = 90
# PRODUCT_H = 90
# PRODUCT_Y = 115


# # ==========================================
# # RANDOM BATCH LOAD
# # ==========================================
# def load_random_batch():
#     def_files = list(TEST_DEF.glob("*.*"))
#     ok_files  = list(TEST_OK.glob("*.*"))

#     total_def = len(def_files)
#     total_ok  = len(ok_files)
#     total_all = total_def + total_ok

#     if total_all == 0:
#         return []

#     p_def = total_def / total_all
#     p_ok  = total_ok  / total_all

#     BATCH_SIZE = random.randint(30, 80)

#     num_def = int(BATCH_SIZE * p_def)
#     num_ok  = BATCH_SIZE - num_def

#     def_sample = random.sample(def_files, min(num_def, total_def))
#     ok_sample  = random.sample(ok_files, min(num_ok, total_ok))

#     all_files = def_sample + ok_sample
#     random.shuffle(all_files)

#     images = []
#     for i, path in enumerate(all_files):
#         clean_img = Image.open(path).convert("RGB")
#         belt_img  = clean_img.convert("RGBA").resize((PRODUCT_W, PRODUCT_H))

#         images.append({
#             "image_name": f"Image {i}",
#             "clean_img": clean_img,
#             "belt_img": belt_img,
#         })
#     return images



# # ==========================================
# # BELT FRAMES
# # ==========================================
# belt_frames = generate_belt_frames()
# BELT_COUNT = len(belt_frames)


# # ==========================================
# # BORDER + LABEL
# # ==========================================
# def add_border_and_label(frame, px, py, pw, ph,
#                          image_name, prediction, confidence, action):

#     img = frame.copy()
#     draw = ImageDraw.Draw(img)

#     if prediction == "OK" and action == "ACCEPT":
#         color = (0, 220, 0)
#     elif prediction == "Defective" and action == "REJECT":
#         color = (220, 0, 0)
#     else:
#         color = (255, 215, 0)

#     for i in range(4):
#         draw.rectangle(
#             [px - i, py - i, px + pw + i, py + ph + i],
#             outline=color
#         )

#     info = (
#         f"{image_name}\n"
#         f"Prediction: {prediction}\n"
#         f"Confidence: {confidence*100:.1f}%\n"
#         f"Action: {action}"
#     )

#     draw.rectangle([10, 10, 350, 115], fill=(0, 0, 0, 160))
#     draw.text((20, 20), info, fill=color)

#     return img



# # ==========================================
# # STREAMLIT PAGE SETUP
# # ==========================================
# st.set_page_config(
#     page_title="Agentic AI – Conveyor Defect Detection",
#     page_icon="🤖",
#     layout="wide",
# )


# # WHITE DASHBOARD STYLE
# st.markdown(
#     """
# <style>
# .stApp {
#     background: white !important;
# }

# /* Top title */
# h1 {
#     font-weight: 800;
# }

# /* Soft card styles */
# .metric-card {
#     padding: 18px;
#     border-radius: 12px;
#     background: white;
#     border: 1px solid #e5e7eb;
#     box-shadow: 0 4px 10px rgba(0,0,0,0.08);
# }

# /* Soft backgrounds */
# .soft-peach   { background: #ffe8d6; }
# .soft-green   { background: #dcfce7; }
# .soft-red     { background: #fee2e2; }
# .soft-blue    { background: #dbeafe; }
# .soft-purple  { background: #e5e7ff; }

# /* Section heading */
# .section-title {
#     font-size: 1.5rem;
#     font-weight: 800;
#     margin-top: 10px;
# }

# /* Final report table */
# .report-container {
#     background: white;
#     padding: 20px;
#     border-radius: 12px;
#     border: 1px solid #e5e7eb;
#     box-shadow: 0 4px 10px rgba(0,0,0,0.1);
# }
# </style>
# """,
#     unsafe_allow_html=True,
# )




# # ==========================================
# # TITLE
# # ==========================================
# st.markdown(
#     "<h1 style='text-align:center;'>🏭 Agentic AI – Defect Detection on Conveyor Belt</h1>",
#     unsafe_allow_html=True,
# )
# st.markdown("---")



# # ==========================================
# # LIVE DETECTION
# # ==========================================
# st.subheader("🎥 Live Detection on Conveyor Belt")

# start = st.button("▶ Start Batch Scan", key="play")

# image_placeholder = st.empty()
# results = []


# # ==========================================
# # MAIN DETECTION LOGIC
# # ==========================================
# if start:

#     test_images = load_random_batch()
#     batch_size = len(test_images)

#     start_time = time.time()

#     for idx, item in enumerate(test_images):

#         clean_img = item["clean_img"]
#         belt_img = item["belt_img"]

#         bw, bh = belt_frames[0].size
#         center_x = bw // 2 - PRODUCT_W // 2

#         # ENTER
#         for x in range(-PRODUCT_W, center_x, 15):
#             belt = belt_frames[x % BELT_COUNT].copy()
#             belt.paste(belt_img, (x, PRODUCT_Y), belt_img)
#             image_placeholder.image(belt, use_container_width=True)
#             time.sleep(0.04)

#         # AGENT WORKFLOW
#         state = run_agents_on_frame(
#             image_name=item["image_name"],
#             frame_id=idx,
#             frame=clean_img,
#         )

#         prediction = state["prediction"]
#         confidence = state["confidence"]
#         action = state["action"]
#         timestamp = state["timestamp"]

#         # SHOW DETECTED
#         frame_center = belt_frames[idx % BELT_COUNT].copy()
#         frame_center.paste(belt_img, (center_x, PRODUCT_Y), belt_img)

#         detected = add_border_and_label(
#             frame_center,
#             center_x, PRODUCT_Y, PRODUCT_W, PRODUCT_H,
#             item["image_name"], prediction, confidence, action
#         )

#         image_placeholder.image(detected, use_container_width=True)
#         time.sleep(0.5)

#         # EXIT
#         for x in range(center_x, bw + PRODUCT_W, 15):
#             belt = belt_frames[x % BELT_COUNT].copy()
#             belt.paste(belt_img, (x, PRODUCT_Y), belt_img)
#             image_placeholder.image(belt, use_container_width=True)
#             time.sleep(0.04)

#         results.append({
#             "Image Name": item["image_name"],
#             "Frame Number": idx,
#             "Prediction": prediction,
#             "Confidence": round(confidence, 4),
#             "Action": action,
#             "Timestamp": timestamp
#         })

#     elapsed = time.time() - start_time
#     speed = round(batch_size / elapsed, 2)

#     df = pd.DataFrame(results)

#     ok_count = (df["Prediction"] == "OK").sum()
#     def_count = (df["Prediction"] == "Defective").sum()
#     avg_conf = df["Confidence"].mean()
#     ok_ratio = ok_count / batch_size


#     # ==========================================
#     # SYSTEM STATUS (LIKE YOUR SCREENSHOT)
#     # ==========================================
#     st.markdown("<div class='section-title'>🛠️ System Status</div>", unsafe_allow_html=True)

#     s1, s2, s3, s4 = st.columns(4)

#     # SYSTEM HEALTH
#     if ok_ratio >= 0.9 and avg_conf >= 0.97:
#         health_text = "🟢 Healthy"
#         health_sub = "High output quality"
#     elif ok_ratio >= 0.75:
#         health_text = "🟡 Warning"
#         health_sub = "Moderate defects"
#     else:
#         health_text = "🔴 Critical"
#         health_sub = "High defects detected"

#     with s1:
#         st.markdown(
#             f"""
#         <div class="metric-card soft-green">
#             <h4>🩺 System Health</h4>
#             <h2>{health_text}</h2>
#             <p>{health_sub}</p>
#         </div>
#         """, unsafe_allow_html=True)

#     # MODEL USED
#     with s2:
#         st.markdown(
#             """
#         <div class="metric-card soft-purple">
#             <h4>🤖 Model Used</h4>
#             <h2>ResNet-18</h2>
#             <p>Version: v1.0</p>
#         </div>
#         """, unsafe_allow_html=True)

#     # AGENT STATUS
#     with s3:
#         st.markdown(
#             """
#         <div class="metric-card soft-blue">
#             <h4>🧩 Agents Status</h4>
#             <h2>Completed</h2>
#             <p>Workflow complete</p>
#         </div>
#         """, unsafe_allow_html=True)

#     # TOTAL TIME
#     with s4:
#         st.markdown(
#             f"""
#         <div class="metric-card soft-peach">
#             <h4>⏱️ Total Time</h4>
#             <h2>{elapsed:.2f} sec</h2>
#             <p>End-to-end processing</p>
#         </div>
#         """, unsafe_allow_html=True)



#     # ==========================================
#     # PRODUCTION STATUS (LIKE SCREENSHOT)
#     # ==========================================
#     st.markdown(f"<div class='section-title'>📦 Production Status (Batch Size: {batch_size})</div>", unsafe_allow_html=True)

#     p1, p2, p3, p4 = st.columns(4)

#     with p1:
#         st.markdown(
#             f"""
#         <div class="metric-card soft-peach">
#             <h4>Total Processed</h4>
#             <h2>{batch_size}</h2>
#             <p>Images inspected</p>
#         </div>
#         """, unsafe_allow_html=True)

#     with p2:
#         st.markdown(
#             f"""
#         <div class="metric-card soft-green">
#             <h4>OK Items</h4>
#             <h2>{ok_count}</h2>
#             <p>Passed inspection</p>
#         </div>
#         """, unsafe_allow_html=True)

#     with p3:
#         st.markdown(
#             f"""
#         <div class="metric-card soft-red">
#             <h4>Defective Items</h4>
#             <h2>{def_count}</h2>
#             <p>Rejected</p>
#         </div>
#         """, unsafe_allow_html=True)

#     with p4:
#         st.markdown(
#             f"""
#         <div class="metric-card soft-blue">
#             <h4>Speed (items/sec)</h4>
#             <h2>{speed}</h2>
#             <p>Average throughput</p>
#         </div>
#         """, unsafe_allow_html=True)



#     # ==========================================
#     # FINAL INSPECTION REPORT
#     # ==========================================
#     st.markdown("<div class='section-title'>📑 Final Inspection Report</div>", unsafe_allow_html=True)

#     df2 = df.copy()

#     def badge_pred(v):
#         if v == "OK":
#             return "<span style='background:#22c55e;color:white;padding:5px 12px;border-radius:12px;'>OK</span>"
#         else:
#             return "<span style='background:#ef4444;color:white;padding:5px 12px;border-radius:12px;'>Defective</span>"

#     def badge_action(v):
#         if v == "ACCEPT":
#             return "<span style='background:#2563eb;color:white;padding:5px 12px;border-radius:12px;'>ACCEPT</span>"
#         else:
#             return "<span style='background:#f59e0b;color:white;padding:5px 12px;border-radius:12px;'>REJECT</span>"

#     df2["Prediction"] = df2["Prediction"].apply(badge_pred)
#     df2["Action"] = df2["Action"].apply(badge_action)

#     st.markdown('<div class="report-container">', unsafe_allow_html=True)
#     st.write(df2.to_html(escape=False, index=False), unsafe_allow_html=True)
#     st.markdown('</div>', unsafe_allow_html=True)



#     # ==========================================
#     # DOWNLOAD BUTTON
#     # ==========================================
#     st.download_button(
#         "⬇ Download Report (CSV)",
#         df.to_csv(index=False),
#         "inspection_report.csv",
#         "text/csv",
#     )

# else:
#     st.info("Click **▶ Start Batch Scan** to begin.")






# import sys
# import random
# import time
# from pathlib import Path

# import streamlit as st
# import pandas as pd
# from PIL import Image, ImageDraw

# # Make src/ importable
# PROJECT_ROOT = Path(__file__).resolve().parent
# SRC_DIR = PROJECT_ROOT / "src"
# sys.path.append(str(SRC_DIR))

# from conveyor_belt import generate_belt_frames
# from agents_graph import run_agents_on_frame


# # ==========================================
# # CONFIG
# # ==========================================
# TEST_DEF = PROJECT_ROOT / "data" / "casting_data" / "test" / "def_front"
# TEST_OK  = PROJECT_ROOT / "data" / "casting_data" / "test" / "ok_front"

# PRODUCT_W = 90
# PRODUCT_H = 90
# PRODUCT_Y = 115


# # ==========================================
# # RANDOM BATCH LOAD
# # ==========================================
# def load_random_batch():
#     def_files = list(TEST_DEF.glob("*.*"))
#     ok_files  = list(TEST_OK.glob("*.*"))

#     total_def = len(def_files)
#     total_ok  = len(ok_files)
#     total_all = total_def + total_ok

#     if total_all == 0:
#         return []

#     p_def = total_def / total_all
#     p_ok  = total_ok  / total_all

#     BATCH_SIZE = random.randint(30, 80)

#     num_def = int(BATCH_SIZE * p_def)
#     num_ok  = BATCH_SIZE - num_def

#     def_sample = random.sample(def_files, min(num_def, total_def))
#     ok_sample  = random.sample(ok_files, min(num_ok, total_ok))

#     all_files = def_sample + ok_sample
#     random.shuffle(all_files)

#     images = []
#     for i, path in enumerate(all_files):
#         clean_img = Image.open(path).convert("RGB")
#         belt_img  = clean_img.convert("RGBA").resize((PRODUCT_W, PRODUCT_H))

#         images.append({
#             "image_name": f"Image {i}",
#             "clean_img": clean_img,
#             "belt_img": belt_img,
#         })
#     return images


# # ==========================================
# # BELT FRAMES
# # ==========================================
# belt_frames = generate_belt_frames()
# BELT_COUNT = len(belt_frames)


# # ==========================================
# # BORDER + LABEL
# # ==========================================
# def add_border_and_label(frame, px, py, pw, ph,
#                          image_name, prediction, confidence, action):

#     img = frame.copy()
#     draw = ImageDraw.Draw(img)

#     if prediction == "OK" and action == "ACCEPT":
#         color = (0, 220, 0)
#     elif prediction == "Defective" and action == "REJECT":
#         color = (220, 0, 0)
#     else:
#         color = (255, 215, 0)

#     for i in range(4):
#         draw.rectangle(
#             [px - i, py - i, px + pw + i, py + ph + i],
#             outline=color
#         )

#     info = (
#         f"{image_name}\n"
#         f"Prediction: {prediction}\n"
#         f"Confidence: {confidence*100:.1f}%\n"
#         f"Action: {action}"
#     )

#     draw.rectangle([10, 10, 350, 115], fill=(0, 0, 0, 160))
#     draw.text((20, 20), info, fill=color)

#     return img


# # ==========================================
# # STREAMLIT PAGE SETUP
# # ==========================================
# st.set_page_config(
#     page_title="Agentic AI – Conveyor Defect Detection",
#     page_icon="🤖",
#     layout="wide",
# )


# # WHITE DASHBOARD THEME
# st.markdown(
#     """
# <style>
# .stApp {
#     background: white !important;
# }

# /* Card layout */
# .metric-card {
#     padding: 20px;
#     border-radius: 12px;
#     background: white;
#     border: 1px solid #e5e7eb;
#     box-shadow: 0 4px 8px rgba(0,0,0,0.06);
# }

# /* Soft pastel fills */
# .soft-peach   { background: #ffe8d6; }
# .soft-green   { background: #dcfce7; }
# .soft-red     { background: #fee2e2; }
# .soft-blue    { background: #dbeafe; }
# .soft-purple  { background: #e5e7ff; }

# /* Section Titles */
# .section-title {
#     font-size: 1.5rem;
#     font-weight: 800;
#     margin-top: 14px;
# }

# </style>
# """,
#     unsafe_allow_html=True,
# )


# # ==========================================
# # TITLE
# # ==========================================
# st.markdown(
#     "<h1 style='text-align:center;'>🏭 Agentic AI – Defect Detection on Conveyor Belt</h1>",
#     unsafe_allow_html=True,
# )
# st.markdown("---")


# # ==========================================
# # LIVE DETECTION
# # ==========================================
# st.subheader("🎥 Live Detection on Conveyor Belt")

# start = st.button("▶ Start Batch Scan", key="play")

# image_placeholder = st.empty()
# results = []


# # ==========================================
# # MAIN DETECTION LOGIC
# # ==========================================
# if start:

#     test_images = load_random_batch()
#     batch_size = len(test_images)

#     start_time = time.time()

#     for idx, item in enumerate(test_images):

#         clean_img = item["clean_img"]
#         belt_img = item["belt_img"]

#         bw, bh = belt_frames[0].size
#         center_x = bw // 2 - PRODUCT_W // 2

#         # ENTER BELT
#         for x in range(-PRODUCT_W, center_x, 15):
#             belt = belt_frames[x % BELT_COUNT].copy()
#             belt.paste(belt_img, (x, PRODUCT_Y), belt_img)
#             image_placeholder.image(belt, use_container_width=True)
#             time.sleep(0.04)

#         # AGENT WORKFLOW
#         state = run_agents_on_frame(
#             image_name=item["image_name"],
#             frame_id=idx,
#             frame=clean_img,
#         )

#         prediction = state["prediction"]
#         confidence = state["confidence"]
#         action = state["action"]
#         timestamp = state["timestamp"]

#         # CENTER POSITION
#         frame_center = belt_frames[idx % BELT_COUNT].copy()
#         frame_center.paste(belt_img, (center_x, PRODUCT_Y), belt_img)

#         detected = add_border_and_label(
#             frame_center,
#             center_x, PRODUCT_Y, PRODUCT_W, PRODUCT_H,
#             item["image_name"], prediction, confidence, action
#         )

#         image_placeholder.image(detected, use_container_width=True)
#         time.sleep(0.5)

#         # EXIT BELT
#         for x in range(center_x, bw + PRODUCT_W, 15):
#             belt = belt_frames[x % BELT_COUNT].copy()
#             belt.paste(belt_img, (x, PRODUCT_Y), belt_img)
#             image_placeholder.image(belt, use_container_width=True)
#             time.sleep(0.04)

#         results.append({
#             "Image Name": item["image_name"],
#             "Frame Number": idx,
#             "Prediction": prediction,
#             "Confidence": round(confidence, 4),
#             "Action": action,
#             "Timestamp": timestamp
#         })

#     elapsed = time.time() - start_time
#     speed = round(batch_size / elapsed, 2)

#     df = pd.DataFrame(results)

#     ok_count = (df["Prediction"] == "OK").sum()
#     def_count = (df["Prediction"] == "Defective").sum()
#     avg_conf = df["Confidence"].mean()
#     ok_ratio = ok_count / batch_size


#     # ==========================================
#     # SYSTEM STATUS
#     # ==========================================
#     st.markdown("<div class='section-title'>🛠️ System Status</div>", unsafe_allow_html=True)

#     s1, s2, s3, s4 = st.columns(4)

#     # HEALTH
#     if ok_ratio >= 0.9 and avg_conf >= 0.97:
#         health = "🟢 Healthy"
#         sub = "High quality output"
#     elif ok_ratio >= 0.75:
#         health = "🟡 Warning"
#         sub = "Moderate defects"
#     else:
#         health = "🔴 Critical"
#         sub = "High defects detected"

#     with s1:
#         st.markdown(
#             f"""
#         <div class="metric-card soft-green">
#             <h4>🩺 System Health</h4>
#             <h2>{health}</h2>
#             <p>{sub}</p>
#         </div>
#         """, unsafe_allow_html=True)

#     # MODEL
#     with s2:
#         st.markdown(
#             """
#         <div class="metric-card soft-purple">
#             <h4>🤖 Model Used</h4>
#             <h2>ResNet-18</h2>
#             <p>Version: v1.0</p>
#         </div>
#         """, unsafe_allow_html=True)

#     # AGENTS STATUS
#     with s3:
#         st.markdown(
#             """
#         <div class="metric-card soft-blue">
#             <h4>🧩 Agents Status</h4>
#             <h2>Completed</h2>
#             <p>Workflow complete</p>
#         </div>
#         """, unsafe_allow_html=True)

#     # TIME
#     with s4:
#         st.markdown(
#             f"""
#         <div class="metric-card soft-peach">
#             <h4>⏱️ Total Time</h4>
#             <h2>{elapsed:.2f} sec</h2>
#             <p>End-to-end processing</p>
#         </div>
#         """, unsafe_allow_html=True)


#     # ==========================================
#     # PRODUCTION STATUS
#     # ==========================================
#     st.markdown(f"<div class='section-title'>📦 Production Status (Batch Size: {batch_size})</div>", unsafe_allow_html=True)

#     p1, p2, p3, p4 = st.columns(4)

#     with p1:
#         st.markdown(
#             f"""
#         <div class="metric-card soft-peach">
#             <h4>Total Processed</h4>
#             <h2>{batch_size}</h2>
#             <p>Images inspected</p>
#         </div>
#         """, unsafe_allow_html=True)

#     with p2:
#         st.markdown(
#             f"""
#         <div class="metric-card soft-green">
#             <h4>OK Items</h4>
#             <h2>{ok_count}</h2>
#             <p>Passed inspection</p>
#         </div>
#         """, unsafe_allow_html=True)

#     with p3:
#         st.markdown(
#             f"""
#         <div class="metric-card soft-red">
#             <h4>Defective Items</h4>
#             <h2>{def_count}</h2>
#             <p>Rejected</p>
#         </div>
#         """, unsafe_allow_html=True)

#     with p4:
#         st.markdown(
#             f"""
#         <div class="metric-card soft-blue">
#             <h4>Speed (items/sec)</h4>
#             <h2>{speed}</h2>
#             <p>Average throughput</p>
#         </div>
#         """, unsafe_allow_html=True)


#     # ==========================================
#     # FINAL INSPECTION REPORT (DATAFRAME)
#     # ==========================================
#     st.markdown("<div class='section-title'>📑 Final Inspection Report</div>", unsafe_allow_html=True)

#     df_display = df.copy()   # clean dataframe

#     st.dataframe(df_display, use_container_width=True)


#     # ==========================================
#     # DOWNLOAD CSV
#     # ==========================================
#     st.download_button(
#         "⬇ Download Report (CSV)",
#         df.to_csv(index=False),
#         "inspection_report.csv",
#         "text/csv",
#     )

# else:
#     st.info("Click **▶ Start Batch Scan** to begin.")



# import sys
# import random
# import time
# from pathlib import Path

# import streamlit as st
# import pandas as pd
# from PIL import Image, ImageDraw

# # Make src/ importable
# PROJECT_ROOT = Path(__file__).resolve().parent
# SRC_DIR = PROJECT_ROOT / "src"
# sys.path.append(str(SRC_DIR))

# from conveyor_belt import generate_belt_frames
# from agents_graph import run_agents_on_frame


# # ==========================================
# # CONFIG
# # ==========================================
# TEST_DEF = PROJECT_ROOT / "data" / "casting_data" / "test" / "def_front"
# TEST_OK  = PROJECT_ROOT / "data" / "casting_data" / "test" / "ok_front"

# PRODUCT_W = 90
# PRODUCT_H = 90
# PRODUCT_Y = 115


# # ==========================================
# # RANDOM BATCH LOAD
# # ==========================================
# def load_random_batch():
#     def_files = list(TEST_DEF.glob("*.*"))
#     ok_files  = list(TEST_OK.glob("*.*"))

#     total_def = len(def_files)
#     total_ok  = len(ok_files)
#     total_all = total_def + total_ok

#     if total_all == 0:
#         return []

#     p_def = total_def / total_all
#     p_ok  = total_ok  / total_all

#     BATCH_SIZE = random.randint(30, 80)

#     num_def = int(BATCH_SIZE * p_def)
#     num_ok  = BATCH_SIZE - num_def

#     def_sample = random.sample(def_files, min(num_def, total_def))
#     ok_sample  = random.sample(ok_files, min(num_ok, total_ok))

#     all_files = def_sample + ok_sample
#     random.shuffle(all_files)

#     images = []
#     for i, path in enumerate(all_files):
#         clean_img = Image.open(path).convert("RGB")
#         belt_img  = clean_img.convert("RGBA").resize((PRODUCT_W, PRODUCT_H))

#         images.append({
#             "image_name": f"Image {i}",
#             "clean_img": clean_img,
#             "belt_img": belt_img,
#         })
#     return images


# # ==========================================
# # BELT FRAMES
# # ==========================================
# belt_frames = generate_belt_frames()
# BELT_COUNT = len(belt_frames)


# # ==========================================
# # BORDER + LABEL
# # ==========================================
# def add_border_and_label(frame, px, py, pw, ph,
#                          image_name, prediction, confidence, action):

#     img = frame.copy()
#     draw = ImageDraw.Draw(img)

#     if prediction == "OK" and action == "ACCEPT":
#         color = (0, 220, 0)
#     elif prediction == "Defective" and action == "REJECT":
#         color = (220, 0, 0)
#     else:
#         color = (255, 215, 0)

#     for i in range(4):
#         draw.rectangle(
#             [px - i, py - i, px + pw + i, py + ph + i],
#             outline=color
#         )

#     info = (
#         f"{image_name}\n"
#         f"Prediction: {prediction}\n"
#         f"Confidence: {confidence*100:.1f}%\n"
#         f"Action: {action}"
#     )

#     draw.rectangle([10, 10, 350, 115], fill=(0, 0, 0, 160))
#     draw.text((20, 20), info, fill=color)

#     return img


# # ==========================================
# # STREAMLIT PAGE SETUP
# # ==========================================
# st.set_page_config(
#     page_title="Agentic AI – Conveyor Defect Detection",
#     page_icon="🤖",
#     layout="wide",
# )

# # ==========================================
# # GLOBAL CSS (including STICKY HEADER)
# # ==========================================
# st.markdown(
#     """
# <style>

# .stApp {
#     background: #f3f4f6 !important;
# }

# /* Sticky title bar */
# .sticky-title {
#     position: sticky;
#     top: 0;
#     z-index: 999;
#     background: #f3f4f6;
#     padding: 18px 0 14px 0;
#     border-bottom: 1px solid #e5e7eb;
# }

# /* Style inside sticky title */
# .sticky-title h1 {
#     text-align: center;
#     font-size: 2rem;
#     font-weight: 800;
#     margin: 0;
# }

# /* Card layout */
# .metric-card {
#     padding: 20px;
#     border-radius: 12px;
#     background: white;
#     border: 1px solid #e5e7eb;
#     box-shadow: 0 4px 8px rgba(0,0,0,0.06);
# }

# /* Soft pastel fills */
# .soft-peach   { background: #ffe8d6; }
# .soft-green   { background: #dcfce7; }
# .soft-red     { background: #fee2e2; }
# .soft-blue    { background: #dbeafe; }
# .soft-purple  { background: #e5e7ff; }

# /* Section Titles */
# .section-title {
#     font-size: 1.5rem;
#     font-weight: 800;
#     margin-top: 14px;
# }

# </style>
# """,
#     unsafe_allow_html=True,
# )


# # ==========================================
# # STICKY TITLE
# # ==========================================
# st.markdown(
#     """
# <div class="sticky-title">
#     <h1>🏭 Agentic AI – Defect Detection on Conveyor Belt</h1>
# </div>
# """,
#     unsafe_allow_html=True,
# )


# # ==========================================
# # LIVE DETECTION
# # ==========================================
# st.subheader("🎥 Live Detection on Conveyor Belt")

# start = st.button("▶ Start Batch Scan", key="play")

# image_placeholder = st.empty()
# results = []


# # ==========================================
# # MAIN DETECTION LOGIC
# # ==========================================
# if start:

#     test_images = load_random_batch()
#     batch_size = len(test_images)

#     start_time = time.time()

#     for idx, item in enumerate(test_images):

#         clean_img = item["clean_img"]
#         belt_img = item["belt_img"]

#         bw, bh = belt_frames[0].size
#         center_x = bw // 2 - PRODUCT_W // 2

#         # ENTER BELT
#         for x in range(-PRODUCT_W, center_x, 15):
#             belt = belt_frames[x % BELT_COUNT].copy()
#             belt.paste(belt_img, (x, PRODUCT_Y), belt_img)
#             image_placeholder.image(belt, use_container_width=True)
#             time.sleep(0.04)

#         # AGENT WORKFLOW
#         state = run_agents_on_frame(
#             image_name=item["image_name"],
#             frame_id=idx,
#             frame=clean_img,
#         )

#         prediction = state["prediction"]
#         confidence = state["confidence"]
#         action = state["action"]
#         timestamp = state["timestamp"]

#         # CENTER POSITION
#         frame_center = belt_frames[idx % BELT_COUNT].copy()
#         frame_center.paste(belt_img, (center_x, PRODUCT_Y), belt_img)

#         detected = add_border_and_label(
#             frame_center,
#             center_x, PRODUCT_Y, PRODUCT_W, PRODUCT_H,
#             item["image_name"], prediction, confidence, action
#         )

#         image_placeholder.image(detected, use_container_width=True)
#         time.sleep(0.5)

#         # EXIT BELT
#         for x in range(center_x, bw + PRODUCT_W, 15):
#             belt = belt_frames[x % BELT_COUNT].copy()
#             belt.paste(belt_img, (x, PRODUCT_Y), belt_img)
#             image_placeholder.image(belt, use_container_width=True)
#             time.sleep(0.04)

#         results.append({
#             "Image Name": item["image_name"],
#             "Frame Number": idx,
#             "Prediction": prediction,
#             "Confidence": round(confidence, 4),
#             "Action": action,
#             "Timestamp": timestamp
#         })

#     elapsed = time.time() - start_time
#     speed = round(batch_size / elapsed, 2)

#     df = pd.DataFrame(results)

#     ok_count = (df["Prediction"] == "OK").sum()
#     def_count = (df["Prediction"] == "Defective").sum()
#     avg_conf = df["Confidence"].mean()
#     ok_ratio = ok_count / batch_size


#     # ==========================================
#     # SYSTEM STATUS
#     # ==========================================
#     st.markdown("<div class='section-title'>🛠️ System Status</div>", unsafe_allow_html=True)

#     s1, s2, s3, s4 = st.columns(4)

#     # HEALTH
#     if ok_ratio >= 0.9 and avg_conf >= 0.97:
#         health = "🟢 Healthy"
#         sub = "High quality output"
#     elif ok_ratio >= 0.75:
#         health = "🟡 Warning"
#         sub = "Moderate defects"
#     else:
#         health = "🔴 Critical"
#         sub = "High defects detected"

#     with s1:
#         st.markdown(
#             f"""
#         <div class="metric-card soft-green">
#             <h4>🩺 System Health</h4>
#             <h2>{health}</h2>
#             <p>{sub}</p>
#         </div>
#         """, unsafe_allow_html=True)

#     # MODEL
#     with s2:
#         st.markdown(
#             """
#         <div class="metric-card soft-purple">
#             <h4>🤖 Model Used</h4>
#             <h2>ResNet-18</h2>
#             <p>Version: v1.0</p>
#         </div>
#         """,
#         unsafe_allow_html=True)

#     # AGENTS STATUS
#     with s3:
#         st.markdown(
#             """
#         <div class="metric-card soft-blue">
#             <h4>🧩 Agents Status</h4>
#             <h2>Completed</h2>
#             <p>Workflow complete</p>
#         </div>
#         """,
#         unsafe_allow_html=True)

#     # TIME
#     with s4:
#         st.markdown(
#             f"""
#         <div class="metric-card soft-peach">
#             <h4>⏱️ Total Time</h4>
#             <h2>{elapsed:.2f} sec</h2>
#             <p>End-to-end processing</p>
#         </div>
#         """,
#         unsafe_allow_html=True)


#     # ==========================================
#     # PRODUCTION STATUS
#     # ==========================================
#     st.markdown(f"<div class='section-title'>📦 Production Status (Batch Size: {batch_size})</div>", unsafe_allow_html=True)

#     p1, p2, p3, p4 = st.columns(4)

#     with p1:
#         st.markdown(
#             f"""
#         <div class="metric-card soft-peach">
#             <h4>Total Processed</h4>
#             <h2>{batch_size}</h2>
#             <p>Images inspected</p>
#         </div>
#         """, unsafe_allow_html=True)

#     with p2:
#         st.markdown(
#             f"""
#         <div class="metric-card soft-green">
#             <h4>OK Items</h4>
#             <h2>{ok_count}</h2>
#             <p>Passed inspection</p>
#         </div>
#         """, unsafe_allow_html=True)

#     with p3:
#         st.markdown(
#             f"""
#         <div class="metric-card soft-red">
#             <h4>Defective Items</h4>
#             <h2>{def_count}</h2>
#             <p>Rejected</p>
#         </div>
#         """, unsafe_allow_html=True)

#     with p4:
#         st.markdown(
#             f"""
#         <div class="metric-card soft-blue">
#             <h4>Speed (items/sec)</h4>
#             <h2>{speed}</h2>
#             <p>Average throughput</p>
#         </div>
#         """, unsafe_allow_html=True)


#     # ==========================================
#     # FINAL INSPECTION REPORT (DATAFRAME)
#     # ==========================================
#     st.markdown("<div class='section-title'>📑 Final Inspection Report</div>", unsafe_allow_html=True)

#     df_display = df.copy()

#     st.dataframe(df_display, use_container_width=True)


#     # ==========================================
#     # DOWNLOAD CSV
#     # ==========================================
#     st.download_button(
#         "⬇ Download Report (CSV)",
#         df.to_csv(index=False),
#         "inspection_report.csv",
#         "text/csv",
#     )

# else:
#     st.info("Click **▶ Start Batch Scan** to begin.")


import sys
import random
import time
from pathlib import Path

import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw

# Make src/ importable
PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
sys.path.append(str(SRC_DIR))

from conveyor_belt import generate_belt_frames
from agents_graph import run_agents_on_frame


# ==========================================
# CONFIG
# ==========================================
TEST_DEF = PROJECT_ROOT / "data" / "casting_data" / "test" / "def_front"
TEST_OK  = PROJECT_ROOT / "data" / "casting_data" / "test" / "ok_front"

PRODUCT_W = 90
PRODUCT_H = 90
PRODUCT_Y = 115


# ==========================================
# RANDOM BATCH LOAD
# ==========================================
def load_random_batch():
    def_files = list(TEST_DEF.glob("*.*"))
    ok_files  = list(TEST_OK.glob("*.*"))

    total_def = len(def_files)
    total_ok  = len(ok_files)
    total_all = total_def + total_ok

    if total_all == 0:
        return []

    p_def = total_def / total_all
    p_ok  = total_ok  / total_all

    BATCH_SIZE = random.randint(30, 80)

    num_def = int(BATCH_SIZE * p_def)
    num_ok  = BATCH_SIZE - num_def

    def_sample = random.sample(def_files, min(num_def, total_def))
    ok_sample  = random.sample(ok_files, min(num_ok, total_ok))

    all_files = def_sample + ok_sample
    random.shuffle(all_files)

    images = []
    for i, path in enumerate(all_files):
        clean_img = Image.open(path).convert("RGB")
        belt_img  = clean_img.convert("RGBA").resize((PRODUCT_W, PRODUCT_H))

        images.append({
            "image_name": f"Image {i}",
            "clean_img": clean_img,
            "belt_img": belt_img,
        })
    return images


# ==========================================
# BELT FRAMES
# ==========================================
belt_frames = generate_belt_frames()
BELT_COUNT = len(belt_frames)


# ==========================================
# BORDER + LABEL
# ==========================================
def add_border_and_label(frame, px, py, pw, ph,
                         image_name, prediction, confidence, action):

    img = frame.copy()
    draw = ImageDraw.Draw(img)

    if prediction == "OK" and action == "ACCEPT":
        color = (0, 220, 0)
    elif prediction == "Defective" and action == "REJECT":
        color = (220, 0, 0)
    else:
        color = (255, 215, 0)

    for i in range(4):
        draw.rectangle(
            [px - i, py - i, px + pw + i, py + ph + i],
            outline=color
        )

    info = (
        f"{image_name}\n"
        f"Prediction: {prediction}\n"
        f"Confidence: {confidence*100:.1f}%\n"
        f"Action: {action}"
    )

    draw.rectangle([10, 10, 350, 115], fill=(0, 0, 0, 160))
    draw.text((20, 20), info, fill=color)

    return img


# ==========================================
# STREAMLIT PAGE SETUP + CUSTOM CSS
# ==========================================
st.set_page_config(
    page_title="Agentic AI – Conveyor Defect Detection",
    page_icon="🤖",
    layout="wide",
)

st.markdown(
    """
<style>

.stApp {
    background: #f3f4f6 !important;
}

/* Sticky title bar */
.sticky-title {
    position: sticky;
    top: 0;
    z-index: 999;
    background: #f3f4f6;
    padding: 18px 0 14px 0;
    border-bottom: 1px solid #e5e7eb;
}

/* Title style */
.sticky-title h1 {
    text-align: center;
    font-size: 2rem;
    font-weight: 800;
    margin: 0;
}

/* Cards */
.metric-card {
    padding: 20px;
    border-radius: 12px;
    background: white;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 8px rgba(0,0,0,0.06);
}

/* Pastel colors */
.soft-peach   { background: #ffe8d6; }
.soft-green   { background: #dcfce7; }
.soft-red     { background: #fee2e2; }
.soft-blue    { background: #dbeafe; }
.soft-purple  { background: #e5e7ff; }

/* Section Title */
.section-title {
    font-size: 1.5rem;
    font-weight: 800;
    margin-top: 14px;
}

</style>
""",
    unsafe_allow_html=True,
)


# ==========================================
# STICKY TITLE
# ==========================================
st.markdown(
    """
<div class="sticky-title">
    <h1>🏭 Agentic AI – Defect Detection on Conveyor Belt</h1>
</div>
""",
    unsafe_allow_html=True,
)


# ==========================================
# LIVE DETECTION
# ==========================================
st.subheader("🎥 Live Detection on Conveyor Belt")

start = st.button("▶ Start Batch Scan", key="play")

image_placeholder = st.empty()
results = []


# ==========================================
# MAIN DETECTION LOGIC
# ==========================================
if start:

    test_images = load_random_batch()
    batch_size = len(test_images)
    start_time = time.time()

    for idx, item in enumerate(test_images):

        clean_img = item["clean_img"]
        belt_img = item["belt_img"]

        bw, bh = belt_frames[0].size
        center_x = bw // 2 - PRODUCT_W // 2

        # ENTER BELT
        for x in range(-PRODUCT_W, center_x, 15):
            belt = belt_frames[x % BELT_COUNT].copy()
            belt.paste(belt_img, (x, PRODUCT_Y), belt_img)
            image_placeholder.image(belt, use_container_width=True)
            time.sleep(0.04)

        # AGENT WORKFLOW
        state = run_agents_on_frame(
            image_name=item["image_name"],
            frame_id=idx,
            frame=clean_img,
        )

        prediction = state["prediction"]
        confidence = state["confidence"]
        action = state["action"]
        timestamp = state["timestamp"]

        # CENTER
        frame_center = belt_frames[idx % BELT_COUNT].copy()
        frame_center.paste(belt_img, (center_x, PRODUCT_Y), belt_img)

        detected = add_border_and_label(
            frame_center, center_x, PRODUCT_Y,
            PRODUCT_W, PRODUCT_H,
            item["image_name"], prediction, confidence, action
        )

        image_placeholder.image(detected, use_container_width=True)
        time.sleep(0.5)

        # EXIT BELT
        for x in range(center_x, bw + PRODUCT_W, 15):
            belt = belt_frames[x % BELT_COUNT].copy()
            belt.paste(belt_img, (x, PRODUCT_Y), belt_img)
            image_placeholder.image(belt, use_container_width=True)
            time.sleep(0.04)

        results.append({
            "Image Name": item["image_name"],
            "Frame Number": idx,
            "Prediction": prediction,
            "Confidence": round(confidence, 4),
            "Action": action,
            "Timestamp": timestamp
        })

    elapsed = time.time() - start_time
    speed = round(batch_size / elapsed, 2)

    df = pd.DataFrame(results)


    # ==========================================
    # SYSTEM STATUS
    # ==========================================
    st.markdown("<div class='section-title'>🛠️ System Status</div>", unsafe_allow_html=True)

    s1, s2, s3, s4 = st.columns(4)

    ok_count = (df["Prediction"] == "OK").sum()
    def_count = (df["Prediction"] == "Defective").sum()
    avg_conf = df["Confidence"].mean()
    ok_ratio = ok_count / batch_size

    if ok_ratio >= 0.9 and avg_conf >= 0.97:
        health = "🟢 Healthy"
        sub = "High quality output"
    elif ok_ratio >= 0.75:
        health = "🟡 Warning"
        sub = "Moderate defects"
    else:
        health = "🔴 Critical"
        sub = "High defects detected"

    with s1:
        st.markdown(f"""
        <div class="metric-card soft-green">
            <h4>🩺 System Health</h4>
            <h2>{health}</h2>
            <p>{sub}</p>
        </div>
        """, unsafe_allow_html=True)

    with s2:
        st.markdown("""
        <div class="metric-card soft-purple">
            <h4>🤖 Model Used</h4>
            <h2>ResNet-18</h2>
            <p>Version: v1.0</p>
        </div>
        """, unsafe_allow_html=True)

    with s3:
        st.markdown("""
        <div class="metric-card soft-blue">
            <h4>🧩 Agents Status</h4>
            <h2>Completed</h2>
            <p>Workflow complete</p>
        </div>
        """, unsafe_allow_html=True)

    with s4:
        st.markdown(f"""
        <div class="metric-card soft-peach">
            <h4>⏱️ Total Time</h4>
            <h2>{elapsed:.2f} sec</h2>
            <p>End-to-end processing</p>
        </div>
        """, unsafe_allow_html=True)


    # ==========================================
    # PRODUCTION STATUS
    # ==========================================
    st.markdown(f"<div class='section-title'>📦 Production Status (Batch Size: {batch_size})</div>",
                unsafe_allow_html=True)

    p1, p2, p3, p4 = st.columns(4)

    with p1:
        st.markdown(f"""
        <div class="metric-card soft-peach">
            <h4>Total Processed</h4>
            <h2>{batch_size}</h2>
            <p>Images inspected</p>
        </div>
        """, unsafe_allow_html=True)

    with p2:
        st.markdown(f"""
        <div class="metric-card soft-green">
            <h4>OK Items</h4>
            <h2>{ok_count}</h2>
            <p>Passed inspection</p>
        </div>
        """, unsafe_allow_html=True)

    with p3:
        st.markdown(f"""
        <div class="metric-card soft-red">
            <h4>Defective Items</h4>
            <h2>{def_count}</h2>
            <p>Rejected</p>
        </div>
        """, unsafe_allow_html=True)

    with p4:
        st.markdown(f"""
        <div class="metric-card soft-blue">
            <h4>Speed (items/sec)</h4>
            <h2>{speed}</h2>
            <p>Average throughput</p>
        </div>
        """, unsafe_allow_html=True)


    # ==========================================
    # FINAL INSPECTION REPORT (HTML-STYLED TABLE)
    # ==========================================
    st.markdown("<div class='section-title'>📑 Final Inspection Report</div>",
                unsafe_allow_html=True)

    df_display = df.copy()

    table_html = df_display.to_html(index=False, classes="styled-table")

    st.markdown("""
    <style>
    .styled-table {
        border-collapse: collapse;
        width: 100%;
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #e5e7eb;
        font-size: 15px;
    }
    .styled-table thead th {
        background-color: #ccfbf1 !important;
        color: #064e3b !important;
        font-weight: 700;
        padding: 12px;
        border-bottom: 2px solid #99f6e4;
    }
    .styled-table td {
        padding: 12px;
        border-bottom: 1px solid #f1f5f9;
    }
    .styled-table tr:nth-child(even) {
        background-color: #f9fafb;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(table_html, unsafe_allow_html=True)


    # ==========================================
    # DOWNLOAD CSV
    # ==========================================
    st.download_button(
        "⬇ Download Report (CSV)",
        df.to_csv(index=False),
        "inspection_report.csv",
        "text/csv",
    )

else:
    st.info("Click **▶ Start Batch Scan** to begin.")









