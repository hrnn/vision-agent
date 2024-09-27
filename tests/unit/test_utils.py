from vision_agent.agent.agent_utils import extract_code, extract_json


def test_basic_json_extract():
    a = '{"a": 1, "b": 2}'
    assert extract_json(a) == {"a": 1, "b": 2}


def test_side_case_quotes_json_extract():
    a = "{'0': 'no', '3': 'no', '6': 'no', '9': 'yes', '12': 'no', '15': 'no'}"
    a_json = extract_json(a)
    assert len(a_json) == 6


def test_side_case_bool_json_extract():
    a = "{'0': False, '3': False, '6': False, '9': True, '12': False, '15': False}"
    a_json = extract_json(a)
    assert len(a_json) == 6


def test_complicated_case_json_extract_1():
    a = """```json {     "plan1": {         "thoughts": "This plan uses the owl_v2_video tool to detect the truck and then uses ocr to read the USDOT and trailer numbers. This approach is efficient as it can process the entire video at once for truck detection.",         "instructions": [             "Use extract_frames to get frames from truck1.mp4",             "Use owl_v2_video with prompt 'truck' to detect if a truck is present in the video",             "If a truck is detected, use ocr on relevant frames to read the USDOT and trailer numbers",             "Process the OCR results to extract the USDOT and trailer numbers",             "Compile results into JSON format and save using save_json"         ]     },     "plan2": {         "thoughts": "This plan uses florence2_sam2_video_tracking to segment and track the truck, then uses florence2_ocr for text detection. This approach might be more accurate for text detection as it can focus on the relevant parts of the truck.",         "instructions": [             "Use extract_frames to get frames from truck1.mp4",             "Use florence2_sam2_video_tracking with prompt 'truck' to segment and track the truck",             "If a truck is segmented, use florence2_ocr on the segmented area to detect text",             "Process the OCR results to extract the USDOT and trailer numbers",             "Compile results into JSON format and save using save_json"         ]     },     "plan3": {         "thoughts": "This plan uses ixc25_video_vqa to directly ask questions about the truck, USDOT number, and trailer number. This approach leverages the model's ability to understand and answer complex questions about video content.",         "instructions": [             "Use extract_frames to get frames from truck1.mp4",             "Use ixc25_video_vqa with the question 'Is there a truck in this video?' to detect the presence of a truck",             "If a truck is present, use ixc25_video_vqa with the question 'What is the USDOT number on the truck?'",             "Use ixc25_video_vqa with the question 'What is the trailer number on the truck?'",             "Process the answers to extract the required information",             "Compile results into JSON format and save using save_json"         ]     } } ```"""

    a_json = extract_json(a)
    assert len(a_json) == 3
    assert "plan1" in a_json


def test_complicated_case_json_extract_2():
    a = """{\n    "predicted_answer": "2",\n    "thoughts": "After analyzing the image and the tool outputs, I can see that there are indeed 2 dogs in the image. One is a small grey dog on the grass, and the other is a larger white dog on the patio. All three plans correctly identified 2 dogs, but I believe plan2 using the countgd_counting tool is the best choice for this task. Here\'s why:\n\n    1. Accuracy: The countgd_counting tool provided high confidence scores (0.92 and 0.9) for both dogs, which aligns with what I can see in the image.\n    \n    2. Precision: The bounding boxes from the countgd_counting tool seem to be more precise and tightly fit around the dogs compared to the other tools.\n    \n    3. Simplicity: While plan3 offers a more complex approach with additional verification, it\'s not necessary in this case as the dogs are clearly visible and easily identifiable. The extra steps in plan3 would add unnecessary complexity and potential for errors.\n    \n    4. Efficiency: Plan2 is more straightforward and efficient than plan3, while potentially offering better accuracy than plan1 (owl_v2_image tool had lower confidence scores).",\n    "best_plan": "plan2"\n}"""
    a_json = extract_json(a)
    assert len(a_json) == 3
    assert "predicted_answer" in a_json


def test_basic_code_extract():
    a = """```python
def test_basic_json_extract():
    a = '{"a": 1, "b": 2}'
    assert extract_json(a) == {"a": 1, "b": 2}
```
"""
    a_code = extract_code(a)
    assert "def test_basic_json_extract():" in a_code
    assert "assert extract_json(a) == {" in a_code