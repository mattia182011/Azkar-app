import json
import os
import flet as ft

# ملف حفظ البيانات محلياً
DATA_FILE = "app_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"tasbeeh_counter": 0, "tasbeeh_total": 0, "selected_dhikr": "سُبْحَانَ اللَّهِ", "counts": {}}

def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def main(page: ft.Page):
    page.title = "أذكاري والسبحة"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.rtl = True
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # تحميل البيانات المحفوظة
    data = load_data()

    # ------------------ 1. قسم السبحة ------------------
    counter_value = data.get("tasbeeh_counter", 0)
    total_value = data.get("tasbeeh_total", 0)
    saved_dhikr = data.get("selected_dhikr", "سُبْحَانَ اللَّهِ")

    counter_text = ft.Text(str(counter_value), size=52, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_700)
    total_text = ft.Text(f"الإجمالي التراكمي: {total_value}", size=14, color=ft.colors.GREY_700)
    current_dhikr = ft.Text(saved_dhikr, size=24, weight=ft.FontWeight.W_600)

    def count_up(e):
        nonlocal counter_value, total_value
        counter_value += 1
        total_value += 1
        counter_text.value = str(counter_value)
        total_text.value = f"الإجمالي التراكمي: {total_value}"
        data["tasbeeh_counter"] = counter_value
        data["tasbeeh_total"] = total_value
        save_data(data)
        page.update()

    def reset_tasbeeh(e):
        nonlocal counter_value
        counter_value = 0
        counter_text.value = "0"
        data["tasbeeh_counter"] = 0
        save_data(data)
        page.update()

    def change_dhikr(e):
        current_dhikr.value = e.control.value
        data["selected_dhikr"] = e.control.value
        save_data(data)
        reset_tasbeeh(None)

    dhikr_dropdown = ft.Dropdown(
        label="اختر الذكر",
        value=saved_dhikr,
        options=[
            ft.dropdown.Option("سُبْحَانَ اللَّهِ"),
            ft.dropdown.Option("الْحَمْدُ لِلَّهِ"),
            ft.dropdown.Option("لا إِلَهَ إِلا اللَّهُ"),
            ft.dropdown.Option("اللَّهُ أَكْبَرُ"),
            ft.dropdown.Option("أَسْتَغْفِرُ اللَّهَ"),
            ft.dropdown.Option("لا حَوْلَ وَلا قُوَّةَ إِلا بِاللَّهِ"),
            ft.dropdown.Option("سُبْحَانَ اللَّهِ وَبِحَمْدِهِ ، سُبْحَانَ اللَّهِ الْعَظِيمِ"),
            ft.dropdown.Option("اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِيِّنَا مُحَمَّدٍ"),
        ],
        on_change=change_dhikr,
        width=300,
    )

    tasbeeh_view = ft.Column(
        controls=[
            ft.Container(height=10),
            dhikr_dropdown,
            ft.Container(height=15),
            current_dhikr,
            ft.Container(
                content=counter_text,
                alignment=ft.alignment.center,
                width=160,
                height=160,
                bgcolor=ft.colors.GREEN_50,
                border_radius=80,
                border=ft.border.all(3, ft.colors.GREEN_400),
            ),
            ft.Container(height=10),
            total_text,
            ft.Container(height=10),
            ft.ElevatedButton(
                "تسبيح",
                icon=ft.icons.TOUCH_APP,
                on_click=count_up,
                width=220,
                height=55,
                bgcolor=ft.colors.GREEN_600,
                color=ft.colors.WHITE,
            ),
            ft.TextButton("تصفير عداد الذكر الحالي", icon=ft.icons.REFRESH, on_click=reset_tasbeeh),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # ------------------ 2. بيانات الأذكار ------------------
    morning_azkar = [
        {"id": "m1", "text": "أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لاَ إِلَهَ إِلاَّ اللَّهُ وَحْدَهُ لاَ شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ.", "count": 1},
        {"id": "m2", "text": "اللَّهُمَّ أَنْتَ رَبِّي لا إِلَهَ إِلا أَنْتَ، خَلَقْتَنِي وَأَنَا عَبْدُكَ، وَأَنَا عَلَى عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ، أَعُوذُ بِكَ مِنْ شَرِّ مَا صَنَعْتُ، أَبُوءُ لَكَ بِنِعْمَتِكَ عَلَيَّ، وَأَبُوءُ بِذَنْبِي فَاغْفِرْ لِي.", "count": 1},
        {"id": "m3", "text": "اللَّهُمَّ بِكَ أَصْبَحْنَا، وَبِكَ أَمْسَيْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ، وَإِلَيْكَ النُّشُورُ.", "count": 1},
        {"id": "m4", "text": "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ: عَدَدَ خَلْقِهِ، وَرِضَا نَفْسِهِ، وَزِنَةَ عَرْشِهِ، وَمِدَادَ كَلِمَاتِهِ.", "count": 3},
        {"id": "m5", "text": "بِسْمِ اللَّهِ الَّذِي لاَ يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الأَرْضِ وَلاَ فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ.", "count": 3},
        {"id": "m6", "text": "رَضِيتُ بِاللَّهِ رَبّاً، وَبِالإِسْلاَمِ دِيناً، وَبِمُحَمَّدٍ صلى الله عليه وسلم نَبِيّاً.", "count": 3},
        {"id": "m7", "text": "يَا حَيُّ يَا قَيُّومُ بِرَحْمَتِكَ أَسْتَغِيثُ، أَصْلِحْ لِي شَأْنِي كُلَّهُ، وَلاَ تَكِلْنِي إِلَى نَفْسِي طَرْفَةَ عَيْنٍ.", "count": 1},
        {"id": "m8", "text": "أَسْتَغْفِرُ اللَّهَ وَأَتُوبُ إِلَيْهِ.", "count": 100},
    ]

    evening_azkar = [
        {"id": "e1", "text": "أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لاَ إِلَهَ إِلاَّ اللَّهُ وَحْدَهُ لاَ شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ.", "count": 1},
        {"id": "e2", "text": "اللَّهُمَّ أَنْتَ رَبِّي لا إِلَهَ إِلا أَنْتَ، خَلَقْتَنِي وَأَنَا عَبْدُكَ، وَأَنَا عَلَى عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ، أَعُوذُ بِكَ مِنْ شَرِّ مَا صَنَعْتُ، أَبُوءُ لَكَ بِنِعْمَتِكَ عَلَيَّ، وَأَبُوءُ بِذَنْبِي فَاغْفِرْ لِي.", "count": 1},
        {"id": "e3", "text": "اللَّهُمَّ بِكَ أَمْسَيْنَا، وَبِكَ أَصْبَحْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ، وَإِلَيْكَ الْمَصِيرُ.", "count": 1},
        {"id": "e4", "text": "أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ.", "count": 3},
        {"id": "e5", "text": "بِسْمِ اللَّهِ الَّذِي لاَ يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الأَرْضِ وَلاَ فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ.", "count": 3},
        {"id": "e6", "text": "رَضِيتُ بِاللَّهِ رَبّاً، وَبِالإِسْلاَمِ دِيناً، وَبِمُحَمَّدٍ صلى الله عليه وسلم نَبِيّاً.", "count": 3},
        {"id": "e7", "text": "يَا حَيُّ يَا قَيُّومُ بِرَحْمَتِكَ أَسْتَغِيثُ، أَصْلِحْ لِي شَأْنِي كُلَّهُ، وَلاَ تَكِلْنِي إِلَى نَفْسِي طَرْفَةَ عَيْنٍ.", "count": 1},
        {"id": "e8", "text": "اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِيِّنَا مُحَمَّدٍ.", "count": 10},
    ]

    saved_counts = data.setdefault("counts", {})

    def build_azkar_view(azkar_data):
        cards = []
        buttons_map = {}

        def reset_all(e):
            for it in azkar_data:
                iid = it["id"]
                saved_counts[iid] = it["count"]
                btn = buttons_map[iid]
                btn.text = f"تكرار: {it['count']}"
                btn.disabled = False
                btn.bgcolor = ft.colors.GREEN_600
            save_data(data)
            page.update()

        cards.append(
            ft.Container(
                padding=5,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(f"عدد الأذكار: {len(azkar_data)}", size=14, weight=ft.FontWeight.W_500),
                        ft.TextButton("إعادة تعيين الكل", icon=ft.icons.REPLAY, on_click=reset_all),
                    ],
                ),
            )
        )

        for item in azkar_data:
            item_id = item["id"]
            rem = saved_counts.get(item_id, item["count"])

            btn = ft.ElevatedButton(
                text=f"تكرار: {rem}" if rem > 0 else "تم ✓",
                disabled=(rem == 0),
                bgcolor=ft.colors.GREY_400 if rem == 0 else ft.colors.GREEN_600,
                color=ft.colors.WHITE,
            )
            buttons_map[item_id] = btn

            def make_handler(it_id, button_ref):
                def handler(e):
                    cur = saved_counts.get(it_id, 1)
                    if cur > 1:
                        cur -= 1
                        button_ref.text = f"تكرار: {cur}"
                    elif cur == 1:
                        cur = 0
                        button_ref.text = "تم ✓"
                        button_ref.disabled = True
                        button_ref.bgcolor = ft.colors.GREY_400
                    saved_counts[it_id] = cur
                    save_data(data)
                    page.update()
                return handler

            btn.on_click = make_handler(item_id, btn)

            cards.append(
                ft.Card(
                    content=ft.Container(
                        padding=15,
                        content=ft.Column(
                            controls=[
                                ft.Text(item["text"], size=16, text_align=ft.TextAlign.RIGHT),
                                ft.Row([btn], alignment=ft.MainAxisAlignment.END),
                            ],
                            spacing=10,
                        ),
                    ),
                    margin=ft.margin.only(bottom=10),
                )
            )

        return ft.ListView(controls=cards, expand=True, padding=10)

    # ------------------ 3. التبويبات ------------------
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="السبحة", icon=ft.icons.FINGERPRINT, content=tasbeeh_view),
            ft.Tab(text="أذكار الصباح", icon=ft.icons.WB_SUNNY, content=build_azkar_view(morning_azkar)),
            ft.Tab(text="أذكار المساء", icon=ft.icons.NIGHTLIGHT_ROUND, content=build_azkar_view(evening_azkar)),
        ],
        expand=True,
    )

    page.add(tabs)

if __name__ == "__main__":
    # تشغيل السيرفر على الشبكة المحلية على البورت 8550
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=8550)