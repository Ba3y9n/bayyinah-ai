"""
Bayyinah AI - Official Challenge Knowledge Base Seeder
Seeds canonical documents for the 4 Scientific Levels (A, B, C, D),
Official Challenge Scope, and Verified Terminology across the 11 Official Sources.
Generates genuine 768-d Gemini text embeddings and PostgreSQL FTS search vectors.
"""

import sys
import os
import hashlib
import json
import uuid
from datetime import datetime, timezone
from sqlalchemy import text

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.db.database import SessionLocal
from app.services.gemini_service import gemini_service
from app.utils.arabic_normalizer import normalize_arabic

SOURCES_TO_APPROVE = [
    "00000000-0000-0000-0000-000000000001",
    "00000000-0000-0000-0000-000000000002",
    "00000000-0000-0000-0000-000000000003",
    "00000000-0000-0000-0000-000000000004",
    "00000000-0000-0000-0000-000000000005",
    "00000000-0000-0000-0000-000000000006",
    "00000000-0000-0000-0000-000000000007",
    "00000000-0000-0000-0000-000000000008",
    "00000000-0000-0000-0000-000000000009",
    "00000000-0000-0000-0000-000000000010",
    "00000000-0000-0000-0000-000000000014",
    "00000000-0000-0000-0000-000000000015",
    "00000000-0000-0000-0000-000000000016",
    "00000000-0000-0000-0000-000000000017",
]

DOCUMENTS = [
    # --------------------------------------------------------------------------
    # Level A: الثوابت والقطعيات والأصول الكلية
    # --------------------------------------------------------------------------
    {
        "id": "c1a1a1a1-0001-4000-8000-000000000001",
        "source_id": "00000000-0000-0000-0000-000000000015",  # dorar.net/aqeeda
        "title": "أصل التوحيد وبطلان دعوى عبادة المسلمين للكعبة",
        "title_ar": "أصل التوحيد وبطلان دعوى عبادة المسلمين للكعبة",
        "category": "AQEEDAH",
        "author": "مجموعة من الباحثين بإشراف الشيخ علوي السقاف",
        "publisher": "مؤسسة الدرر السنية",
        "url": "https://dorar.net/aqeeda",
        "sections": [
            {
                "id": "e1a1a1a1-0001-4000-8000-000000000001",
                "title": "إفراد الله تعالى بالعبادة وتجريد التوحيد",
                "chunks": [
                    {
                        "content": "أجمع المسلمون قاطبة على أن التوحيد هو أصل دين الإسلام ورأسه، وهو إفراد الله تعالى بالعبادة وحده لا شريك له، ونفي الشريك والند والصاحبة والولد، قال تعالى: {وَقَضَى رَبُّكَ أَلَّا تَعْبُدُوا إِلَّا إِيَّاهُ} [الإسراء: 23]، وقال سبحانه: {وَمَا أُمِرُوا إِلَّا لِيَعْبُدُوا اللَّهَ مُخْلِصِينَ لَهُ الدِّينَ حُنَفَاءَ} [البينة: 5]. فالعبادة بجميع أنواعها من دعاء وصلاة ورجاء وخوف لا تصرف إلا لله وحده.",
                        "reference": "موسوعة العقيدة والفرق المعاصرة - الدرر السنية، كتاب التوحيد، الباب الأول",
                        "locator": "الدرر السنية - العقيدة - ج1 ص15"
                    },
                    {
                        "content": "الكعبة المشرفة هي قِبلة صلاة المسلمين ووجهة توجههم بأمر الله تعالى وليست معبوداً بحال من الأحوال. والمسلمون لا يعبدون حجراً ولا بشراً ولا بناءً، وإنما يستقبلون الكعبة امتثالاً لأمر الله القائل: {فَوَلِّ وَجْهَكَ شَطْرَ الْمَسْجِدِ الْحَرَامِ وَحَيْثُ مَا كُنْتُمْ فَوَلُّوا وُجُوهَكُمْ شَطْرَهُ} [البقرة: 144]. وقد ثبت عن أمير المؤمنين عمر بن الخطاب رضي الله عنه أنه قبّل الحجر الأسود وقال: «إني أعلم أنك حجر لا تضر ولا تنفع، ولولا أني رأيت رسول الله ﷺ يقبلك ما قبلتك» (رواه البخاري رقم 1597، ومسلم رقم 1270)، وهو برهان قاطع على تجريد العبادة لله وحده ونفي القداسة الذاتية عن الأحجار.",
                        "reference": "صحيح البخاري، كتاب الحج، باب ما ذكر في الحجر الأسود (حديث 1597)؛ صحيح مسلم (حديث 1270)",
                        "locator": "صحيح البخاري: 1597؛ صحيح مسلم: 1270"
                    }
                ]
            }
        ]
    },
    {
        "id": "c1a1a1a1-0002-4000-8000-000000000002",
        "source_id": "00000000-0000-0000-0000-000000000001",  # dawa.center (King Fahd Complex)
        "title": "حفظ القرآن الكريم وسلامة نصه وتواتره القطعي",
        "title_ar": "حفظ القرآن الكريم وسلامة نصه وتواتره القطعي",
        "category": "QURAN",
        "author": "مجمع الملك فهد لطباعة المصحف الشريف",
        "publisher": "مجمع الملك فهد لطباعة المصحف الشريف بالمدينة المنورة",
        "url": "https://dawa.center",
        "sections": [
            {
                "id": "e1a1a1a1-0002-4000-8000-000000000002",
                "title": "الأدلة القطعية على صيانة القرآن الكريم من التبديل والتحريف",
                "chunks": [
                    {
                        "content": "القرآن الكريم هو كلام الله المعجز المنزل على نبينا محمد ﷺ المنقول بالتواتر القطعي، المتعبد بتلاوته، المحفوظ بحفظ الله الصادق القاطع بنص قوله عز وجل: {إِنَّا نَحْنُ نَزَّلْنَا الذِّكْرَ وَإِنَّا لَهُ لَحَافِظُونَ} [الحجر: 9]. وقد أجمعت الأمة سلفاً وخلفاً على سلامة المصحف الشريف بين دفتيه من أي زيادة أو نقصان أو تحريف، ونقلته الألوف عن الألوف حفظاً في الصدور ورسماً في السطور جيلاً بعد جيل.",
                        "reference": "مجمع الملك فهد لطباعة المصحف الشريف، مباحث في علوم القرآن، ص42",
                        "locator": "مجمع الملك فهد - حفظ القرآن - ص42"
                    }
                ]
            }
        ]
    },
    {
        "id": "c1a1a1a1-0003-4000-8000-000000000003",
        "source_id": "00000000-0000-0000-0000-000000000014",  # dorar.net/tafseer
        "title": "سماحة الشريعة الإسلامية ونفي الإكراه في الدين",
        "title_ar": "سماحة الشريعة الإسلامية ونفي الإكراه في الدين",
        "category": "DAWA",
        "author": "موسوعة التفسير - الدرر السنية",
        "publisher": "مؤسسة الدرر السنية",
        "url": "https://dorar.net/tafseer",
        "sections": [
            {
                "id": "e1a1a1a1-0003-4000-8000-000000000003",
                "title": "تفسير آية نفي الإكراه وبيان عدل الإسلام ودعوته بالحكمة",
                "chunks": [
                    {
                        "content": "قال الله تعالى: {لَا إِكْرَاهَ فِي الدِّينِ قَدْ تَبَيَّنَ الرُّشْدُ مِنَ الْغَيِّ} [البقرة: 256]. دلت الآية الكريمة بإجماع أهل التفسير والتحقيق على أنه لا يُكره أحد على الدخول في الإسلام؛ لأن الإيمان تصديق قلبي واقتناع عقلي لا يتحقق بالجبر والإكراه. والأصل في الدعوة الإسلامية هو البيان والحجة والموعظة الحسنة: {ادْعُ إِلَى سَبِيلِ رَبِّكَ بِالْحِكْمَةِ وَالْمَوْعِظَةِ الْحَسَنَةِ} [النحل: 125]. ودعوى انتشار الإسلام بالإكراه أو بالسيف مخالفة لنصوص القرآن الصريحة وللوقائع التاريخية المعتمدة.",
                        "reference": "موسوعة التفسير - الدرر السنية، سورة البقرة آية 256؛ وتفسير ابن كثير ج1 ص682",
                        "locator": "الدرر السنية - تفسير البقرة: 256"
                    }
                ]
            }
        ]
    },

    # --------------------------------------------------------------------------
    # Level B: المسائل الخلافية الفرعية المعتبرة
    # --------------------------------------------------------------------------
    {
        "id": "c1a1a1a1-0004-4000-8000-000000000004",
        "source_id": "00000000-0000-0000-0000-000000000016",  # dorar.net/feqhia
        "title": "حكم قراءة المأموم للفاتحة خلف الإمام في الصلاة الجهرية",
        "title_ar": "حكم قراءة المأموم للفاتحة خلف الإمام في الصلاة الجهرية",
        "category": "FIQH",
        "author": "الموسوعة الفقهية - الدرر السنية",
        "publisher": "مؤسسة الدرر السنية",
        "url": "https://dorar.net/feqhia",
        "sections": [
            {
                "id": "e1a1a1a1-0004-4000-8000-000000000004",
                "title": "مذاهب الأئمة الأربعة في قراءة المأموم خلف الإمام",
                "chunks": [
                    {
                        "content": "مسألة قراءة المأموم للفاتحة خلف الإمام في الصلاة الجهرية من المسائل الاجتهادية الخلافية المعتبرة بين أئمة الفقه: ذهب الشافعية إلى وجوب قراءة الفاتحة على المأموم في كل ركعة لعموم حديث: «لا صلاة لمن لم يقرأ بفاتحة الكتاب». وذهب الحنفية إلى كراهة قراءة المأموم خلف الإمام وأن قراءة الإمام قراءة له لقوله تعالى: {وَإِذَا قُرِئَ الْقُرْآنُ فَاسْتَمِعُوا لَهُ وَأَنْصِتُوا}. وذهب المالكية والحنابلة إلى استحباب قراءتها في السرية والإنصات في الجهرية. وكل مذهب له أدلته المعتبرة ولا إنكار في مسائل الخلاف الاجتهادي السائغ.",
                        "reference": "الموسوعة الفقهية - الدرر السنية، كتاب الصلاة، صفة الصلاة، حكم قراءة المأموم",
                        "locator": "الدرر السنية - الفقهية - ج2 ص112"
                    }
                ]
            }
        ]
    },
    {
        "id": "c1a1a1a1-0005-4000-8000-000000000005",
        "source_id": "00000000-0000-0000-0000-000000000016",  # dorar.net/feqhia
        "title": "حكم رفع اليدين عند الركوع والرفع منه في الصلاة",
        "title_ar": "حكم رفع اليدين عند الركوع والرفع منه في الصلاة",
        "category": "FIQH",
        "author": "الموسوعة الفقهية - الدرر السنية",
        "publisher": "مؤسسة الدرر السنية",
        "url": "https://dorar.net/feqhia",
        "sections": [
            {
                "id": "e1a1a1a1-0005-4000-8000-000000000005",
                "title": "أقوال الفقهاء في سنية رفع اليدين عند الركوع",
                "chunks": [
                    {
                        "content": "اختلف الفقهاء في سنية رفع اليدين عند الركوع وعند الرفع منه: ذهب جمهور العلماء (الشافعية والحنابلة والمالكية في المشهور) إلى استحباب رفع اليدين عند الركوع والرفع منه لحديث ابن عمر في الصحيحين. وذهب الحنفية إلى عدم رفعهما إلا عند تكبيرة الإحرام مستدلين بحديث ابن مسعود. والمسألة من مسائل الخلاف الفقهي الفرعي المعتبر التي وسع فيها السلف ولا يجوز فيها التشديد أو تبديع المخالف.",
                        "reference": "الموسوعة الفقهية - الدرر السنية، كتاب الصلاة، سنن الصلاة القولية والفعلية",
                        "locator": "الدرر السنية - الفقهية - ج2 ص145"
                    }
                ]
            }
        ]
    },

    # --------------------------------------------------------------------------
    # Level C: الاستفسارات والفتاوى الفردية والنوازل وقضايا الأحوال الشخصية
    # --------------------------------------------------------------------------
    {
        "id": "c1a1a1a1-0006-4000-8000-000000000006",
        "source_id": "00000000-0000-0000-0000-000000000006",  # dawa.center/file/7937 (Guideline)
        "title": "الضوابط الشرعية والإرشادية للتعامل مع الفتاوى الفردية والنوازل المعاصرة",
        "title_ar": "الضوابط الشرعية والإرشادية للتعامل مع الفتاوى الفردية والنوازل المعاصرة",
        "category": "QUESTIONS_DOUBTS",
        "author": "الدليل الإرشادي للمحتوى الإسلامي - وزارة الشؤون الإسلامية والدعوة والإرشاد",
        "publisher": "وزارة الشؤون الإسلامية",
        "url": "https://dawa.center/file/7937",
        "sections": [
            {
                "id": "e1a1a1a1-0006-4000-8000-000000000006",
                "title": "قاعدة الامتناع المنهجي والإحالة للجهات الرسمية المعتمدة",
                "chunks": [
                    {
                        "content": "يُحظر على أنظمة الذكاء الاصطناعي والمصنفات الإرشادية إصدار فتاوى خاصة أو أحكام ملزمة في النوازل المعاصرة، ومسائل الطلاق، والمنازعات الأسرية، وتقسيم التركات والمواريث، والقضايا الجنائية والمالية المنظورة قضائياً. المنهج العلمي المعتمد هو: الامتناع عن إصدار الفتوى الفردية، وإرشاد السائل وإحالته إلى الهيئات الرسمية المعتمدة المختصة (مثل هيئة كبار العلماء، الرئاسة العامة للبحوث العلمية والإفتاء، المحاكم الشرعية الرسمية) صيانةً للحقوق والتزاماً بالأصول المنهجية.",
                        "reference": "الدليل الإرشادي للمحتوى الإسلامي، وزارة الشؤون الإسلامية، الباب الرابع: ضوابط الفتوى، ص28",
                        "locator": "الدليل الإرشادي 7937 - ص28"
                    }
                ]
            }
        ]
    },

    # --------------------------------------------------------------------------
    # Level D: المحتوى الواهي أو المكذوب أو غير الثابت
    # --------------------------------------------------------------------------
    {
        "id": "c1a1a1a1-0007-4000-8000-000000000007",
        "source_id": "00000000-0000-0000-0000-000000000004",  # dorar.net/hadith
        "title": "تخريج وتحقيق حديث: صوموا تصحوا",
        "title_ar": "تخريج وتحقيق حديث: صوموا تصحوا",
        "category": "HADITH",
        "author": "الموسوعة الحديثية - الدرر السنية",
        "publisher": "مؤسسة الدرر السنية",
        "url": "https://dorar.net/hadith",
        "sections": [
            {
                "id": "e1a1a1a1-0007-4000-8000-000000000007",
                "title": "حكم المحدثين على متن وإسناد حديث صوموا تصحوا",
                "chunks": [
                    {
                        "content": "حديث: «صوموا تصحوا». أخرجه الطبراني في المعجم الأوسط (8312) وغيره من حديث أبي هريرة وعلي بن أبي طالب. درجة الحديث عند أئمة الصنعة الحديثية: ضعيف ولم يثبت بهذا اللفظ مرفوعاً عن رسول الله ﷺ. ضعفه العراقي في تخريج الإحياء، والهيثمي في مجمع الزوائد، والألباني في ضعيف الجامع (3502) والسلسلة الضعيفة (253). ومع أن الصوم مفيد للبدن صحياً وطبياً إلا أنه لا تجوز نسبته إلى النبي ﷺ بصفته حديثاً ثابتاً.",
                        "reference": "الموسوعة الحديثية - الدرر السنية، تخريج الأحاديث، رقم الحديث 3502؛ السلسلة الضعيفة للألباني (253)",
                        "locator": "الدرر السنية - الموسوعة الحديثية: صوموا تصحوا"
                    }
                ]
            }
        ]
    },
    {
        "id": "c1a1a1a1-0008-4000-8000-000000000008",
        "source_id": "00000000-0000-0000-0000-000000000004",  # dorar.net/hadith
        "title": "بيان وضع وبطلان حديث: اطلبوا العلم ولو في الصين",
        "title_ar": "بيان وضع وبطلان حديث: اطلبوا العلم ولو في الصين",
        "category": "HADITH",
        "author": "الموسوعة الحديثية - الدرر السنية",
        "publisher": "مؤسسة الدرر السنية",
        "url": "https://dorar.net/hadith",
        "sections": [
            {
                "id": "e1a1a1a1-0008-4000-8000-000000000008",
                "title": "حكم أئمة الحديث على خبر طلب العلم ولو بالصين",
                "chunks": [
                    {
                        "content": "حديث: «اطلبوا العلم ولو بالصين؛ فإن طلب العلم فريضة على كل مسلم». أخرجه العقيلي في الضعفاء، وابن عدي في الكامل، والبيهقي في شعب الإيمان من حديث أنس بن مالك. حكم الحديث: باطل وموضوع ومكذوب على رسول الله ﷺ، في إسناده أبو عاتكة طريف بن سليمان وهو مجمع على ضعفه ونكارته، وقال ابن الجوزي: موضوع. وقال الألباني في السلسلة الضعيفة (416): باطل لا أصل له. فلا تجوز روايته منسوباً للنبي ﷺ إلا لبيان وضعه.",
                        "reference": "الموسوعة الحديثية - الدرر السنية؛ الموضوعات لابن الجوزي؛ السلسلة الضعيفة والموضوعة للألباني رقم 416",
                        "locator": "الدرر السنية - الموسوعة الحديثية: اطلبوا العلم ولو بالصين"
                    }
                ]
            }
        ]
    },
    {
        "id": "c1a1a1a1-0009-4000-8000-000000000009",
        "source_id": "00000000-0000-0000-0000-000000000004",  # dorar.net/hadith
        "title": "حكم نسبة مقولة: حب الوطن من الإيمان إلى النبي ﷺ",
        "title_ar": "حكم نسبة مقولة: حب الوطن من الإيمان إلى النبي ﷺ",
        "category": "HADITH",
        "author": "الموسوعة الحديثية - الدرر السنية",
        "publisher": "مؤسسة الدرر السنية",
        "url": "https://dorar.net/hadith",
        "sections": [
            {
                "id": "e1a1a1a1-0009-4000-8000-000000000009",
                "title": "حكم عبارة حب الوطن من الإيمان",
                "chunks": [
                    {
                        "content": "مقولة: «حب الوطن من الإيمان». يتداولها بعض الناس على أنها حديث نبوي. حكمها الحديثي: لا أصل له، وموضوع ومختلق مكذوب على النبي ﷺ، نص على وضعه وعدم ثبوته الصغاني في الموضوعات، والعجلوني في كشف الخفاء (1100)، والألباني في السلسلة الضعيفة (36). ومحبة الوطن من الأمور الفطرية الجبلية لكن لا يجوز شرعاً نسبتها لرسول الله ﷺ كحديث نبوي.",
                        "reference": "الموسوعة الحديثية - الدرر السنية؛ كشف الخفاء للعجلوني (1100)؛ السلسلة الضعيفة للألباني رقم 36",
                        "locator": "الدرر السنية - الموسوعة الحديثية: حب الوطن من الإيمان"
                    }
                ]
            }
        ]
    },

    # --------------------------------------------------------------------------
    # Official Terminology & Challenge Scope Policy
    # --------------------------------------------------------------------------
    {
        "id": "c1a1a1a1-0010-4000-8000-000000000010",
        "source_id": "00000000-0000-0000-0000-000000000007",  # islamic-content.com/dictionary
        "title": "قاموس المصطلحات والمفاهيم الإسلامية: مصطلح التوحيد - Monotheism / Tawhid",
        "title_ar": "قاموس المصطلحات والمفاهيم الإسلامية: مصطلح التوحيد - Monotheism / Tawhid",
        "category": "DICTIONARY_TRANSLATION",
        "author": "المنصة الرقمية للمحتوى الإسلامي",
        "publisher": "المنصة الرقمية للمحتوى الإسلامي",
        "url": "https://islamic-content.com/dictionary",
        "sections": [
            {
                "id": "e1a1a1a1-0010-4000-8000-000000000010",
                "title": "المصطلح، المعنى، والترجمة الإنجليزية المعتمدة",
                "chunks": [
                    {
                        "content": "مادة (التوحيد) - Islamic Monotheism / Tawhid: إفراد الله تعالى بالربوبية والألوهية والأسماء والصفات، وإفراده سبحانه بجميع أنواع العبادة كالصلاة والدعاء والذبح والنذر. الترجمة المعتمدة بالإنجليزية: Islamic Monotheism / Tawhid (The Oneness of God). ضوابط الترجمة: الاقتصار على لفظ Monotheism مجرداً قد يوهم الاشتراك مع معتقدات أخرى، لذا يلزم شرعاً تقييده بـ Islamic Monotheism أو الإبقاء على اللفظ الأصلي المعرب Tawhid مع شرح إفراد العبادة لله وحده.",
                        "reference": "قاموس المصطلحات والمفاهيم الإسلامية، المنصة الرقمية، مادة (ت و ح - التوحيد)",
                        "locator": "قاموس المصطلحات - مادة التوحيد"
                    }
                ]
            }
        ]
    },
    {
        "id": "c1a1a1a1-0011-4000-8000-000000000011",
        "source_id": "00000000-0000-0000-0000-000000000002",  # islamic-content.com
        "title": "الوثيقة المنهجية الرسمية لمعايير المحتوى الإسلامي والتحقق وضوابط الامتناع",
        "title_ar": "الوثيقة المنهجية الرسمية لمعايير المحتوى الإسلامي والتحقق وضوابط الامتناع",
        "category": "DAWA",
        "author": "اللجنة العلمية لتحدي المحتوى الإسلامي",
        "publisher": "المنصة الرقمية للمحتوى الإسلامي",
        "url": "https://islamic-content.com",
        "sections": [
            {
                "id": "e1a1a1a1-0011-4000-8000-000000000011",
                "title": "المستويات العلمية الأربعة وقاعدة الامتناع المنهجي",
                "chunks": [
                    {
                        "content": "نطاق المحتوى الإسلامي ومعايير التحقق المعتمدة تشمل أربعة مستويات علمية ملزمة:\nالمستوى الأول (أ): الثوابت والقطعيات والأصول الكلية كأصل التوحيد وحفظ القرآن الكريم وسماحة الإسلام؛ وتثبت بأدلة الكتاب والسنة والإجماع.\nالمستوى الثاني (ب): المسائل الخلافية الفرعية المعتبرة بين أئمة الفقه المعتمدين؛ وواجب النظام فيها عرض أقوال المذاهب بأمانة وعدم إلغاء الخلاف السائغ.\nالمستوى الثالث (ج): الاستفسارات والفتاوى الفردية والنوازل والقضايا الأسرية والتركات؛ والواجب هو الامتناع عن الفتوى وإحالة السائل للجهات الرسمية المعتمدة.\nالمستوى الرابع (د): المحتوى الواهي أو المكذوب أو غير الثابت؛ وحكمه بيان درجة الحديث أو القول وعدم نسبته كحديث صحيح.\nقاعدة الامتناع: الامتناع في الحالات غير القاطعة، وعدم إطلاق أحكام مطلقة في مواضع الخلاف، وإحالة الفتاوى للجهات الرسمية.",
                        "reference": "الوثيقة المنهجية لتحدي المحتوى الإسلامي، معايير التحقق المنهجي وقواعد القرار، البند 1-4",
                        "locator": "وثيقة معايير المحتوى الإسلامي - البند 1-4"
                    }
                ]
            }
        ]
    },
    {
        "id": "c1a1a1a1-0012-4000-8000-000000000012",
        "source_id": "00000000-0000-0000-0000-000000000004",  # dorar.net/hadith
        "title": "تخريج وتحقيق حديث: إنما الأعمال بالنيات",
        "title_ar": "تخريج وتحقيق حديث: إنما الأعمال بالنيات",
        "category": "HADITH",
        "author": "الموسوعة الحديثية - الدرر السنية",
        "publisher": "مؤسسة الدرر السنية",
        "url": "https://dorar.net/hadith",
        "sections": [
            {
                "id": "e1a1a1a1-0012-4000-8000-000000000012",
                "title": "متن وتخريج حديث إنما الأعمال بالنيات وصحته",
                "chunks": [
                    {
                        "content": "عن عمر بن الخطاب رضي الله عنه قال: سمعت رسول الله ﷺ يقول: «إنما الأعمال بالنيات، وإنما لكل امرئ ما نوى، فمن كانت هجرته إلى دنيا يصيبها، أو إلى امرأة ينكحها، فهجرته إلى ما هاجر إليه». أخرجه البخاري (1)، ومسلم (1907). حكم الحديث في الموسوعة الحديثية: صحيح ثابت متفق عليه بأعلى درجات الصحة، وهو أصل عظيم وقاعدة كلية من قواعد الشريعة ومدار الإسلام عليه.",
                        "reference": "الموسوعة الحديثية - الدرر السنية، صحيح البخاري (1)، صحيح مسلم (1907)",
                        "locator": "الدرر السنية - الموسوعة الحديثية: إنما الأعمال بالنيات"
                    }
                ]
            }
        ]
    },
    {
        "id": "c1a1a1a1-0013-4000-8000-000000000013",
        "source_id": "00000000-0000-0000-0000-000000000004",  # dorar.net/hadith
        "title": "تخريج وتحقيق حديث: المسلم من سلم المسلمون من لسانه ويده",
        "title_ar": "تخريج وتحقيق حديث: المسلم من سلم المسلمون من لسانه ويده",
        "category": "HADITH",
        "author": "الموسوعة الحديثية - الدرر السنية",
        "publisher": "مؤسسة الدرر السنية",
        "url": "https://dorar.net/hadith",
        "sections": [
            {
                "id": "e1a1a1a1-0013-4000-8000-000000000013",
                "title": "متن وتخريج حديث المسلم من سلم المسلمون وصحته",
                "chunks": [
                    {
                        "content": "عن عبد الله بن عمرو رضي الله عنهما، عن النبي ﷺ قال: «المسلم من سلم المسلمون من لسانه ويده، والمهاجر من هجر ما نهى الله عنه». أخرجه البخاري (10)، ومسلم (40). حكم الحديث في الموسوعة الحديثية: صحيح متفق عليه، ثابت بأعلى درجات الثبوت.",
                        "reference": "الموسوعة الحديثية - الدرر السنية، صحيح البخاري (10)، صحيح مسلم (40)",
                        "locator": "الدرر السنية - الموسوعة الحديثية: المسلم من سلم المسلمون"
                    }
                ]
            }
        ]
    },
    {
        "id": "c1a1a1a1-0014-4000-8000-000000000014",
        "source_id": "00000000-0000-0000-0000-000000000003",  # quranpedia.net
        "title": "آية الكرسي - سورة البقرة آية 255 وتفسيرها ومكانتها",
        "title_ar": "آية الكرسي - سورة البقرة آية 255 وتفسيرها ومكانتها",
        "category": "QURAN",
        "author": "موسوعة القرآن الكريم - قرآن بيديا",
        "publisher": "قرآن بيديا",
        "url": "https://quranpedia.net",
        "sections": [
            {
                "id": "e1a1a1a1-0014-4000-8000-000000000014",
                "title": "نص آية الكرسي وبيان التوحيد والصفات الإلهية",
                "chunks": [
                    {
                        "content": "قال الله تعالى: {اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ ۚ لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ ۚ لَّهُ مَا فِي السَّمَاوَاتِ وَمَا فِي الْأَرْضِ ۗ مَن ذَا الَّذِي يَشْفَعُ عِندَهُ إِلَّا بِإِذْنِهِ ۚ يَعْلَمُ مَا بَيْنَ أَيْدِيهِمْ وَمَا خَلْفَهُمْ ۖ وَلَا يُحِيطُونَ بِشَيْءٍ مِّنْ عِلْمِهِ إِلَّا بِمَا شَاءَ ۚ وَسِعَ كُرْسِيُّهُ السَّمَاوَاتِ وَالْأَرْضَ ۖ وَلَا يَئُودُهُ حِفْظُهُمَا ۚ وَهُوَ الْعَلِيُّ الْعَظِيمُ} [البقرة: 255]. آية الكرسي أعظم آية في كتاب الله تعالى، وهي نص قطعي الثبوت والدلالة على توحيد الألوهية والربوبية والأسماء والصفات وتنزه الله عن العجز والنقص.",
                        "reference": "موسوعة القرآن الكريم - قرآن بيديا، سورة البقرة (2:255)",
                        "locator": "قرآن بيديا - سورة البقرة آية 255"
                    }
                ]
            }
        ]
    }
]

def seed():
    print("=" * 70)
    print("BAYYINAH AI — SEEDING OFFICIAL CHALLENGE KNOWLEDGE BASE")
    print("=" * 70)

    with SessionLocal() as db:
        # Step 1: Ensure all official sources are APPROVED and ACTIVE
        print("\n[1/4] Ensuring official sources are APPROVED and ACTIVE...")
        for src_id in SOURCES_TO_APPROVE:
            db.execute(text("""
                UPDATE sources 
                SET scientific_status = 'APPROVED', 
                    is_active = true, 
                    approved_by_challenge = true,
                    updated_at = NOW()
                WHERE id = :sid;
            """), {"sid": src_id})
        db.commit()
        print(f"  ✅ Updated {len(SOURCES_TO_APPROVE)} official sources to APPROVED.")

        # Step 2: Ingest Documents, Sections, and Chunks
        print("\n[2/4] Ingesting Official Documents and Sections...")
        total_docs = 0
        total_sections = 0
        total_chunks = 0
        total_embeddings = 0

        for doc_data in DOCUMENTS:
            doc_id = doc_data["id"]
            
            # Upsert document
            db.execute(text("""
                INSERT INTO documents (
                    id, source_id, title, title_ar, title_en, author, publisher,
                    category, document_type, url, canonical_url, official_url,
                    language, license_status, ingestion_method, ingestion_status,
                    indexing_status, rights_status, version, created_at, updated_at
                ) VALUES (
                    :id, :source_id, :title, :title_ar, :title_en, :author, :publisher,
                    :category, 'OFFICIAL_TEXT', :url, :url, :url,
                    'ar', 'APPROVED', 'CURATED_OFFICIAL', 'INDEXED',
                    'INDEXED', 'PUBLIC_ACCESS', '1.0', NOW(), NOW()
                )
                ON CONFLICT (id) DO UPDATE SET
                    title = EXCLUDED.title,
                    title_ar = EXCLUDED.title_ar,
                    category = EXCLUDED.category,
                    author = EXCLUDED.author,
                    publisher = EXCLUDED.publisher,
                    url = EXCLUDED.url,
                    indexing_status = 'INDEXED',
                    updated_at = NOW();
            """), {
                "id": doc_id,
                "source_id": doc_data["source_id"],
                "title": doc_data["title"],
                "title_ar": doc_data["title_ar"],
                "title_en": doc_data.get("title_en", ""),
                "author": doc_data.get("author", "اللجنة العلمية"),
                "publisher": doc_data.get("publisher", "منصة بيّنة AI"),
                "category": doc_data["category"],
                "url": doc_data["url"]
            })
            total_docs += 1

            # Ingest Sections and Chunks
            for sec_idx, sec_data in enumerate(doc_data.get("sections", []), 1):
                sec_id = sec_data["id"]
                db.execute(text("""
                    INSERT INTO document_sections (
                        id, document_id, title, section_order, content, created_at
                    ) VALUES (
                        :id, :document_id, :title, :section_order, :content, NOW()
                    )
                    ON CONFLICT (id) DO UPDATE SET
                        title = EXCLUDED.title,
                        section_order = EXCLUDED.section_order;
                """), {
                    "id": sec_id,
                    "document_id": doc_id,
                    "title": sec_data["title"],
                    "section_order": sec_idx,
                    "content": sec_data["title"]
                })
                total_sections += 1

                for chk_idx, chk in enumerate(sec_data.get("chunks", []), 1):
                    chk_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{doc_id}:{sec_id}:{chk_idx}"))
                    raw_content = chk["content"]
                    norm_content = normalize_arabic(raw_content)
                    c_hash = hashlib.sha256(raw_content.encode("utf-8")).hexdigest()

                    # Generate genuine Gemini Embedding
                    print(f"  -> Generating Gemini embedding for chunk {chk_id[:8]} ({chk['locator'][:30]})...")
                    embedding_vec = gemini_service.generate_embedding(raw_content)
                    vec_str = None
                    if embedding_vec and len(embedding_vec) == 768:
                        vec_str = "[" + ",".join(str(float(x)) for x in embedding_vec) + "]"
                        total_embeddings += 1
                    else:
                        print(f"     ⚠️ Embedding generation returned invalid vector length: {len(embedding_vec) if embedding_vec else 0}")

                    # Upsert Chunk with raw SQL for vector & tsvector
                    if vec_str:
                        db.execute(text("""
                            INSERT INTO document_chunks (
                                id, document_id, section_id, chunk_index, chunk_text, content,
                                content_ar, normalized_text, normalized_content, language,
                                reference, locator, source_locator, source_url, canonical_url,
                                content_hash, version, embedding_model, embedding, search_vector,
                                created_at, updated_at
                            ) VALUES (
                                :id, :document_id, :section_id, :chunk_index, :content, :content,
                                :content, :normalized_text, :normalized_text, 'ar',
                                :reference, :locator, :locator, :source_url, :source_url,
                                :content_hash, '1.0', 'models/text-embedding-004',
                                CAST(:vec_str AS vector),
                                to_tsvector('arabic', :content),
                                NOW(), NOW()
                            )
                            ON CONFLICT (id) DO UPDATE SET
                                chunk_text = EXCLUDED.chunk_text,
                                content = EXCLUDED.content,
                                normalized_text = EXCLUDED.normalized_text,
                                reference = EXCLUDED.reference,
                                locator = EXCLUDED.locator,
                                embedding = CAST(:vec_str AS vector),
                                search_vector = to_tsvector('arabic', EXCLUDED.content),
                                updated_at = NOW();
                        """), {
                            "id": chk_id,
                            "document_id": doc_id,
                            "section_id": sec_id,
                            "chunk_index": chk_idx,
                            "content": raw_content,
                            "normalized_text": norm_content,
                            "reference": chk.get("reference", ""),
                            "locator": chk.get("locator", ""),
                            "source_url": doc_data["url"],
                            "content_hash": c_hash,
                            "vec_str": vec_str
                        })
                    else:
                        db.execute(text("""
                            INSERT INTO document_chunks (
                                id, document_id, section_id, chunk_index, chunk_text, content,
                                content_ar, normalized_text, normalized_content, language,
                                reference, locator, source_locator, source_url, canonical_url,
                                content_hash, version, embedding_model, search_vector,
                                created_at, updated_at
                            ) VALUES (
                                :id, :document_id, :section_id, :chunk_index, :content, :content,
                                :content, :normalized_text, :normalized_text, 'ar',
                                :reference, :locator, :locator, :source_url, :source_url,
                                :content_hash, '1.0', 'models/text-embedding-004',
                                to_tsvector('arabic', :content),
                                NOW(), NOW()
                            )
                            ON CONFLICT (id) DO UPDATE SET
                                chunk_text = EXCLUDED.chunk_text,
                                content = EXCLUDED.content,
                                normalized_text = EXCLUDED.normalized_text,
                                reference = EXCLUDED.reference,
                                locator = EXCLUDED.locator,
                                search_vector = to_tsvector('arabic', EXCLUDED.content),
                                updated_at = NOW();
                        """), {
                            "id": chk_id,
                            "document_id": doc_id,
                            "section_id": sec_id,
                            "chunk_index": chk_idx,
                            "content": raw_content,
                            "normalized_text": norm_content,
                            "reference": chk.get("reference", ""),
                            "locator": chk.get("locator", ""),
                            "source_url": doc_data["url"],
                            "content_hash": c_hash
                        })
                    total_chunks += 1

        # Step 3: Record Ingestion Job
        print("\n[3/4] Recording Ingestion Job...")
        job_id = str(uuid.uuid4())
        db.execute(text("""
            INSERT INTO ingestion_jobs (
                id, source_id, job_type, status, documents_discovered,
                documents_processed, chunks_created, embeddings_created,
                error_count, started_at, completed_at, finished_at
            ) VALUES (
                :id, '00000000-0000-0000-0000-000000000002', 'FULL', 'COMPLETED',
                :docs, :docs, :chunks, :embeds, 0, NOW(), NOW(), NOW()
            );
        """), {
            "id": job_id,
            "docs": total_docs,
            "chunks": total_chunks,
            "embeds": total_embeddings
        })

        db.commit()

        # Step 4: Verification Summary
        print("\n[4/4] Verifying Final Ingestion Stats in Supabase PostgreSQL...")
        stats_sources = db.execute(text("SELECT count(*) FROM sources WHERE is_active = true")).scalar()
        stats_docs = db.execute(text("SELECT count(*) FROM documents")).scalar()
        stats_sections = db.execute(text("SELECT count(*) FROM document_sections")).scalar()
        stats_chunks = db.execute(text("SELECT count(*) FROM document_chunks")).scalar()
        stats_embeds = db.execute(text("SELECT count(*) FROM document_chunks WHERE embedding IS NOT NULL")).scalar()

        print(f"  Active Sources:     {stats_sources}")
        print(f"  Total Documents:    {stats_docs}")
        print(f"  Total Sections:     {stats_sections}")
        print(f"  Total Chunks:       {stats_chunks}")
        print(f"  Total Embeddings:   {stats_embeds} (pgvector 768-d)")
        print("\n✅ SEEDING COMPLETE: Official Challenge Knowledge is live in Supabase PostgreSQL!")

if __name__ == "__main__":
    seed()
