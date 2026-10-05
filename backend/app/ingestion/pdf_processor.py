"""
Bayyinah AI - High-Volume PDF Ingestion Processor
Enforces Section 19 of Master Specifications:
Supports massive scholarly PDF documents (> 1000 pages) by auto-splitting into sub-units
(e.g., pages 1-600, 601-1200, 1201-1800) preserving page_start and page_end coordinates.
Prevents memory exhaustion and enables granular citation to specific page numbers.
"""

import io
import logging
from typing import List, Dict, Any, Optional
from pypdf import PdfReader

logger = logging.getLogger("bayyinah.ingestion.pdf_processor")

class PDFProcessor:
    @staticmethod
    def process_scholarly_pdf(
        pdf_bytes: bytes,
        title: str,
        chunk_page_size: int = 600
    ) -> List[Dict[str, Any]]:
        """
        Parses scholarly PDF and auto-splits documents exceeding chunk_page_size.
        Preserves page_start, page_end, and extracts text per section.
        """
        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            total_pages = len(reader.pages)
            logger.info(f"Processing PDF '{title}' with {total_pages} pages.")

            chunks: List[Dict[str, Any]] = []

            # If document is within threshold, process as single unit or normal pages
            if total_pages <= chunk_page_size:
                full_text = []
                for p_idx, page in enumerate(reader.pages):
                    page_text = page.extract_text() or ""
                    if page_text.strip():
                        full_text.append(f"[صفحة {p_idx+1}]\n{page_text}")

                chunks.append({
                    "title": title,
                    "page_start": 1,
                    "page_end": total_pages,
                    "total_pages": total_pages,
                    "part_index": 1,
                    "total_parts": 1,
                    "text_content": "\n\n".join(full_text)
                })
                return chunks

            # Auto-split into sub-units of chunk_page_size
            total_parts = (total_pages + chunk_page_size - 1) // chunk_page_size
            for part_idx in range(total_parts):
                start_p = part_idx * chunk_page_size + 1
                end_p = min((part_idx + 1) * chunk_page_size, total_pages)

                part_text = []
                for p_num in range(start_p, end_p + 1):
                    page = reader.pages[p_num - 1]
                    p_txt = page.extract_text() or ""
                    if p_txt.strip():
                        part_text.append(f"[صفحة {p_num}]\n{p_txt}")

                sub_title = f"{title} (الجزء {part_idx + 1}: الصفحات {start_p}-{end_p})"
                chunks.append({
                    "title": sub_title,
                    "page_start": start_p,
                    "page_end": end_p,
                    "total_pages": total_pages,
                    "part_index": part_idx + 1,
                    "total_parts": total_parts,
                    "text_content": "\n\n".join(part_text)
                })
                logger.info(f"Created sub-chunk: {sub_title} ({len(part_text)} pages extracted)")

            return chunks
        except Exception as e:
            logger.error(f"Failed to process PDF {title}: {e}")
            raise RuntimeError(f"Scholarly PDF processing failed: {str(e)}")

    @staticmethod
    def extract_pdf_pages(
        pdf_bytes: bytes,
        filename: str = "document.pdf",
        max_bytes: int = 100 * 1024 * 1024
    ) -> List[Dict[str, Any]]:
        """
        Extracts pages from uploaded PDF document preserving page_number and text.
        Handles corrupt or non-PDF input gracefully by raising ValueError.
        """
        if not pdf_bytes or len(pdf_bytes) == 0:
            raise ValueError("الملف المرفوع فارغ.")

        if len(pdf_bytes) > max_bytes:
            raise ValueError(f"حجم الوثيقة المرفوعة ({len(pdf_bytes)/(1024*1024):.1f}MB) يتجاوز الحد المسموح به لبيئة التشغيل الحالية ({max_bytes/(1024*1024):.0f}MB).")

        if not pdf_bytes.startswith(b"%PDF"):
            raise ValueError("صيغة الملف غير صالحة، يرجى رفع ملف PDF صحيح.")

        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            total_pages = len(reader.pages)
            if total_pages == 0:
                raise ValueError("ملف PDF لا يحتوي على أي صفحات.")

            pages: List[Dict[str, Any]] = []
            for p_idx, page in enumerate(reader.pages):
                txt = (page.extract_text() or "").strip()
                pages.append({
                    "page_number": p_idx + 1,
                    "text": txt,
                    "file_name": filename,
                    "char_count": len(txt)
                })
            return pages
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error parsing PDF '{filename}': {e}")
            raise ValueError(f"تعذر استخراج النص من ملف PDF: {str(e)}")

pdf_processor = PDFProcessor()
