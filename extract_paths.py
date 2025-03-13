#!/usr/bin/env python3
"""
extract_paths.py

For every XML file in the "Input" folder, parse the Appium/iOS page source,
and output a text file in the "Output" folder with a list of elements.

For each element, the script prints:
  - Its tag name and attributes (name, label, value, etc.)
  - Positional info (x, y, width, height) if present
  - A naive absolute XPath locator
  - Candidate iOS Class Chain locators based on available attributes
  - A classification of "Interactive" vs. "Non-Interactive"

Additionally:
  - A master file "master_interactive.txt" is created in the "Output" folder
    containing all unique "Interactive" elements from all page sources.

Usage:
    python extract_paths.py

Folder structure (same folder as this script):
    ./Input
    ./Output
"""

import os
import xml.etree.ElementTree as ET

INPUT_FOLDER = "Input"
OUTPUT_FOLDER = "Output"
MASTER_FILE = "master_interactive.txt"

# A set of known iOS UI element types that are typically clickable or otherwise interactive.
# This is just a starting point – add or remove as needed.
INTERACTIVE_TAGS = {
    "XCUIElementTypeButton",
    "XCUIElementTypeLink",
    "XCUIElementTypeCell",
    "XCUIElementTypeStaticText",   # Sometimes used like buttons
    "XCUIElementTypeMenuItem",
    "XCUIElementTypeCheckBox",
    "XCUIElementTypeSwitch",
    # Add more if your app uses different tags for clickable elements
}


def main():
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # Keep track of unique interactive elements across all XMLs
    # We'll store them here and write them out at the end.
    master_interactive_set = set()
    master_interactive_items = []

    for filename in os.listdir(INPUT_FOLDER):
        if not filename.lower().endswith(".xml"):
            continue  # Only process XML files

        input_path = os.path.join(INPUT_FOLDER, filename)
        base_name, _ = os.path.splitext(filename)
        output_filename = f"{base_name}_output.txt"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        print(f"Processing {input_path} -> {output_path}")

        try:
            tree = ET.parse(input_path)
            root = tree.getroot()
        except Exception as e:
            print(f"Error parsing {input_path}: {e}")
            continue

        lines = []
        lines.append(f"=== Locators for {filename} ===\n")

        for elem in root.iter():
            # Gather relevant info
            xpath = get_xpath(elem, root)
            ios_class_chain_candidates = get_ios_class_chain_candidates(elem)
            attr_summary = get_attributes_summary(elem)
            position_summary = get_position_summary(elem)
            classification = classify_element(elem)  # "Interactive" or "Non-Interactive"

            # Build element description block
            line_parts = [
                f"Tag: {elem.tag}",
                f"Attributes: {attr_summary}",
            ]
            if position_summary:
                line_parts.append(f"Position: {position_summary}")
            line_parts.append(f"Classification: {classification}")
            line_parts.append(f"Absolute XPath: {xpath}")

            if ios_class_chain_candidates:
                line_parts.append("iOS Class Chain Candidates:")
                for candidate in ios_class_chain_candidates:
                    line_parts.append(f"  - {candidate}")

            lines.append("\n".join(line_parts))
            lines.append("-" * 80)

            # If interactive, consider adding to the master file
            if classification == "Interactive":
                # Build a unique key to avoid duplicates
                unique_key = create_unique_key(elem)
                if unique_key not in master_interactive_set:
                    master_interactive_set.add(unique_key)
                    # Build a line summarizing this element
                    master_line = build_interactive_line(elem, xpath, ios_class_chain_candidates)
                    master_interactive_items.append(master_line)

        # Write out the per-file results
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    # Write the master file of all unique interactive elements
    master_path = os.path.join(OUTPUT_FOLDER, MASTER_FILE)
    with open(master_path, "w", encoding="utf-8") as mf:
        mf.write("=== MASTER LIST OF UNIQUE INTERACTIVE ELEMENTS ===\n\n")
        for item in master_interactive_items:
            mf.write(item + "\n\n")

    print(f"\nMaster interactive file created at: {master_path}")
    print("Extraction complete.")


def classify_element(elem):
    """
    Returns either "Interactive" or "Non-Interactive" based on:
      1) If the tag is in INTERACTIVE_TAGS, AND
      2) The 'enabled' and 'visible' attributes are "true" (if they exist).

    You can tweak these rules as needed.
    """
    tag = elem.tag
    enabled = elem.attrib.get("enabled", "").lower() == "true"
    visible = elem.attrib.get("visible", "").lower() == "true"

    # If 'enabled'/'visible' aren't present, default them to True
    # so we don't exclude elements that don't specify these attributes
    if "enabled" not in elem.attrib:
        enabled = True
    if "visible" not in elem.attrib:
        visible = True

    if tag in INTERACTIVE_TAGS and enabled and visible:
        return "Interactive"
    else:
        return "Non-Interactive"


def create_unique_key(elem):
    """
    Builds a unique key (tuple) for the given element, including:
      - tag, name, label, value
      - x, y, width, height
    You can expand this if needed (e.g., add XPath).
    """
    return (
        elem.tag,
        elem.attrib.get("name", ""),
        elem.attrib.get("label", ""),
        elem.attrib.get("value", ""),
        elem.attrib.get("x", ""),
        elem.attrib.get("y", ""),
        elem.attrib.get("width", ""),
        elem.attrib.get("height", ""),
    )


def build_interactive_line(elem, xpath, ios_class_chain_candidates):
    """
    Builds a multi-line string summarizing an interactive element
    for inclusion in the master file.
    """
    name = elem.attrib.get("name", "")
    label = elem.attrib.get("label", "")
    value = elem.attrib.get("value", "")
    x = elem.attrib.get("x", "")
    y = elem.attrib.get("y", "")
    w = elem.attrib.get("width", "")
    h = elem.attrib.get("height", "")

    lines = [
        f"Tag: {elem.tag}",
        f"name='{name}', label='{label}', value='{value}'",
        f"Position: x={x}, y={y}, width={w}, height={h}",
        f"Absolute XPath: {xpath}",
    ]
    if ios_class_chain_candidates:
        lines.append("iOS Class Chain Candidates:")
        for candidate in ios_class_chain_candidates:
            lines.append(f"  - {candidate}")
    return "\n".join(lines)


def get_position_summary(elem):
    """
    Returns a string of positional attributes if present (x, y, width, height).
    """
    x = elem.attrib.get("x")
    y = elem.attrib.get("y")
    w = elem.attrib.get("width")
    h = elem.attrib.get("height")

    position_attrs = []
    if x is not None:
        position_attrs.append(f"x={x}")
    if y is not None:
        position_attrs.append(f"y={y}")
    if w is not None:
        position_attrs.append(f"width={w}")
    if h is not None:
        position_attrs.append(f"height={h}")

    return ", ".join(position_attrs) if position_attrs else ""


def get_attributes_summary(elem):
    """
    Returns a summary string of selected attributes.
    """
    attrs = []
    for key in ["name", "label", "value", "enabled", "visible"]:
        val = elem.attrib.get(key)
        if val:
            attrs.append(f"{key}='{val}'")
    return ", ".join(attrs)


def get_xpath(element, root):
    """
    Builds a naive absolute XPath from the root to 'element'.
    Uses the element's tag name and index among siblings.
    """
    if element == root:
        return f"/{root.tag}"

    segments = []
    current = element
    while current is not None and current != root:
        parent = current.getparent() if hasattr(current, "getparent") else find_parent(root, current)
        if parent is None:
            break

        siblings = [e for e in list(parent) if e.tag == current.tag]
        index = siblings.index(current) + 1  # XPath is 1-indexed
        segments.append(f"/{current.tag}[{index}]")
        current = parent
    segments.reverse()
    return "".join(segments)


def find_parent(root, child):
    """
    Since xml.etree.ElementTree does not provide getparent(),
    we do a recursive search to find the parent of 'child'.
    """
    for elem in root.iter():
        if child in list(elem):
            return elem
    return None


def get_ios_class_chain_candidates(elem):
    """
    Returns a list of candidate iOS Class Chain locator strings based on common attributes:
      - If the element has a 'name' attribute, candidate: **/{tag}[@name='value']
      - If it has a 'label', candidate: **/{tag}[@label='value']
      - If it has a 'value', candidate: **/{tag}[@value='value']
      - If it has both 'name' and 'label', we combine them.
    """
    candidates = []
    tag = elem.tag
    name = elem.attrib.get("name")
    label = elem.attrib.get("label")
    value = elem.attrib.get("value")
    
    if name:
        candidates.append(f"**/{tag}[@name='{name}']")
    if label and (not name or label != name):
        candidates.append(f"**/{tag}[@label='{label}']")
    if value:
        candidates.append(f"**/{tag}[@value='{value}']")
    if name and label:
        candidates.append(f"**/{tag}[@name='{name}' and @label='{label}']")
    
    return candidates


if __name__ == "__main__":
    main()
