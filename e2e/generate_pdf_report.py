#!/usr/bin/env python3
"""
Generate PDF test report for change management documentation.

Parses behave JSON results and embeds screenshots to create a
professional PDF report suitable for change management approval.
"""

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


class TestReportGenerator:
    def __init__(self, json_path: Path, screenshots_dir: Path, output_path: Path):
        self.json_path = json_path
        self.screenshots_dir = screenshots_dir
        self.output_path = output_path
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        self.story = []

    def _setup_custom_styles(self) -> None:
        """Create custom paragraph styles."""
        self.styles.add(
            ParagraphStyle(
                name="CustomTitle",
                parent=self.styles["Heading1"],
                fontSize=24,
                textColor=colors.HexColor("#2C3E50"),
                spaceAfter=30,
                alignment=1,  # Center
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="SectionHeader",
                parent=self.styles["Heading2"],
                fontSize=16,
                textColor=colors.HexColor("#34495E"),
                spaceAfter=12,
                spaceBefore=12,
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="ScenarioTitle",
                parent=self.styles["Heading3"],
                fontSize=14,
                textColor=colors.HexColor("#2980B9"),
                spaceAfter=6,
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="StepText",
                parent=self.styles["Normal"],
                fontSize=11,
                leftIndent=20,
                spaceAfter=4,
            )
        )

    def _add_title_page(self, data: dict[str, Any]) -> None:
        """Add title page with test summary."""
        self.story.append(Spacer(1, 2 * inch))
        self.story.append(Paragraph("End-to-End Test Report", self.styles["CustomTitle"]))
        self.story.append(Spacer(1, 0.5 * inch))

        # Test metadata
        metadata = [
            ["Project:", "Keystone"],
            ["Test Type:", "E2E BDD Tests"],
            ["Test Date:", datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")],
            ["Environment:", "Development"],
        ]

        table = Table(metadata, colWidths=[2 * inch, 4 * inch])
        table.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 12),
                    ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#2C3E50")),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]
            )
        )
        self.story.append(table)
        self.story.append(Spacer(1, 0.5 * inch))

        # Test summary
        total_scenarios = len(data[0]["elements"])
        passed_scenarios = sum(
            1
            for scenario in data[0]["elements"]
            if all(step["result"]["status"] == "passed" for step in scenario["steps"])
        )
        failed_scenarios = total_scenarios - passed_scenarios

        summary = [
            ["Total Scenarios:", str(total_scenarios)],
            ["Passed:", str(passed_scenarios)],
            ["Failed:", str(failed_scenarios)],
            [
                "Success Rate:",
                f"{(passed_scenarios / total_scenarios * 100):.1f}%"
                if total_scenarios > 0
                else "N/A",
            ],
        ]

        summary_table = Table(summary, colWidths=[2 * inch, 2 * inch])
        summary_table.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 12),
                    ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#2C3E50")),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#ECF0F1")),
                ]
            )
        )
        self.story.append(summary_table)
        self.story.append(PageBreak())

    def _sanitize_filename(self, name: str) -> str:
        """Sanitize filename by removing invalid characters."""
        # Replace invalid characters with underscores
        invalid_chars = '":<>|*?\r\n'
        for char in invalid_chars:
            name = name.replace(char, "_")
        # Replace spaces with underscores and collapse multiple underscores
        name = name.replace(" ", "_")
        while "__" in name:
            name = name.replace("__", "_")
        return name

    def _find_screenshot(
        self, scenario_name: str, step_keyword: str, step_name: str
    ) -> Path | None:
        """Find screenshot for a step."""
        # Match the naming pattern from environment.py
        step_screenshot = f"{scenario_name}_{step_keyword}_{step_name}"
        sanitized = self._sanitize_filename(step_screenshot)

        for ext in [".png", ".jpg", ".jpeg"]:
            screenshot_path = self.screenshots_dir / f"{sanitized}{ext}"
            if screenshot_path.exists():
                return screenshot_path

        return None

    def _add_scenario(self, scenario: dict[str, Any]) -> None:
        """Add a scenario with its steps and screenshots."""
        scenario_name = scenario["name"]
        self.story.append(Paragraph(f"Scenario: {scenario_name}", self.styles["ScenarioTitle"]))
        self.story.append(Spacer(1, 0.1 * inch))

        # Scenario description if available
        if scenario.get("description"):
            self.story.append(Paragraph(scenario["description"], self.styles["Normal"]))
            self.story.append(Spacer(1, 0.1 * inch))

        # Steps
        for step in scenario["steps"]:
            keyword = step["keyword"].strip()
            name = step["name"]
            status = step["result"]["status"]

            # Step text with status indicator
            status_color = colors.green if status == "passed" else colors.red
            step_text = f'<font color="{status_color.hexval()}">●</font> {keyword} {name}'
            self.story.append(Paragraph(step_text, self.styles["StepText"]))

            # Add screenshot if it exists for "Then" steps or failures
            if keyword.lower() == "then" or status == "failed":
                screenshot_path = self._find_screenshot(scenario_name, keyword, name)
                if screenshot_path and screenshot_path.exists():
                    self.story.append(Spacer(1, 0.1 * inch))
                    try:
                        # Resize image to fit page width
                        img = Image(str(screenshot_path), width=5.5 * inch, height=3.5 * inch)
                        img.hAlign = "LEFT"
                        self.story.append(img)
                        self.story.append(Spacer(1, 0.1 * inch))
                    except Exception as e:
                        print(f"Warning: Could not embed screenshot {screenshot_path}: {e}")

            # Show error message if failed
            if status == "failed" and "error_message" in step["result"]:
                error_style = ParagraphStyle(
                    name="Error",
                    parent=self.styles["Normal"],
                    fontSize=9,
                    textColor=colors.red,
                    leftIndent=40,
                    fontName="Courier",
                )
                error_text = step["result"]["error_message"][:500]  # Truncate long errors
                self.story.append(Paragraph(f"<b>Error:</b> {error_text}", error_style))

        self.story.append(Spacer(1, 0.3 * inch))

    def _add_approval_section(self) -> None:
        """Add change management approval section."""
        self.story.append(PageBreak())
        self.story.append(Paragraph("Test Approval & Sign-off", self.styles["SectionHeader"]))
        self.story.append(Spacer(1, 0.2 * inch))

        approval_data = [
            ["Role", "Name", "Signature", "Date"],
            ["Test Engineer", "", "", ""],
            ["QA Lead", "", "", ""],
            ["Product Owner", "", "", ""],
            ["Change Manager", "", "", ""],
        ]

        approval_table = Table(
            approval_data, colWidths=[1.5 * inch, 2 * inch, 2 * inch, 1.5 * inch]
        )
        approval_table.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 11),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#34495E")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [colors.white, colors.HexColor("#F8F9FA")],
                    ),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                    ("TOPPADDING", (0, 0), (-1, -1), 12),
                ]
            )
        )
        self.story.append(approval_table)

    def generate(self) -> None:
        """Generate the PDF report."""
        # Load test results
        with Path(self.json_path).open() as f:
            data = json.load(f)

        # Create PDF
        doc = SimpleDocTemplate(
            str(self.output_path),
            pagesize=letter,
            rightMargin=0.75 * inch,
            leftMargin=0.75 * inch,
            topMargin=0.75 * inch,
            bottomMargin=0.75 * inch,
        )

        # Build content
        self._add_title_page(data)

        # Add feature description
        feature = data[0]
        self.story.append(Paragraph(f"Feature: {feature['name']}", self.styles["SectionHeader"]))
        if feature.get("description"):
            # Description can be a list or string
            desc = feature["description"]
            if isinstance(desc, list):
                desc = " ".join(desc)
            self.story.append(Paragraph(desc, self.styles["Normal"]))
        self.story.append(Spacer(1, 0.2 * inch))

        # Add each scenario
        for scenario in feature["elements"]:
            self._add_scenario(scenario)

        # Add approval section
        self._add_approval_section()

        # Generate PDF
        doc.build(self.story)
        print(f"PDF report generated: {self.output_path}")


def main() -> None:
    """Main entry point."""
    json_path = Path("reports/behave-results.json")
    screenshots_dir = Path("screenshots")
    output_path = Path("reports/test-report.pdf")

    if not json_path.exists():
        print(f"Error: JSON results not found at {json_path}")
        print("Run tests with: just e2e-pdf to generate results")
        sys.exit(1)

    generator = TestReportGenerator(json_path, screenshots_dir, output_path)
    generator.generate()


if __name__ == "__main__":
    main()
