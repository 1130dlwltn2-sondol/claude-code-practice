#!/usr/bin/env python3
"""Claude Code 실전 책용 이미지 생성 스크립트 (PIL 기반)."""
import os
import math
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")

BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

BG = (13, 19, 38)
PANEL = (24, 33, 62)
CORAL = (224, 120, 86)
TEAL = (78, 205, 196)
BLUE = (96, 150, 255)
WHITE = (245, 247, 250)
MUTED = (154, 167, 199)
LINE = (70, 88, 140)
LIGHT_BG = (250, 251, 253)
INK = (30, 41, 59)
SUB = (100, 116, 139)
CARD_LINE = (203, 213, 225)


def font(path, size):
    return ImageFont.truetype(path, size, index=1)


def text_center(d, cx, y, s, f, fill):
    bb = d.textbbox((0, 0), s, font=f)
    w = bb[2] - bb[0]
    d.text((cx - w / 2 - bb[0], y), s, font=f, fill=fill)


def rrect(d, box, radius, fill, outline=None, width=1):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow(d, x1, y1, x2, y2, fill=CORAL, width=4):
    d.line([x1, y1, x2, y2], fill=fill, width=width)
    ang = math.atan2(y2 - y1, x2 - x1)
    sz = 14
    for da in (2.6, -2.6):
        d.line([x2, y2, x2 + sz * math.cos(ang + da), y2 + sz * math.sin(ang + da)],
               fill=fill, width=width)


# ---------------------------------------------------------------- 표지 1000x1300
def make_cover():
    W, H = 1000, 1300
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        r = int(13 + (30 - 13) * t)
        g = int(19 + (44 - 19) * t)
        b = int(38 + (82 - 38) * t)
        d.line([(0, y), (W, y)], fill=(r, g, b))
    d.ellipse([-180, -180, 320, 320], outline=(224, 120, 86, 90), width=3)
    d.ellipse([-120, -120, 260, 260], outline=(78, 205, 196, 70), width=2)
    d.ellipse([760, 980, 1180, 1400], outline=(96, 150, 255, 80), width=3)
    d.ellipse([820, 1040, 1120, 1340], outline=(224, 120, 86, 60), width=2)
    for i in range(6):
        x = 700 + i * 45
        d.line([(x, 0), (x + 220, 420)], fill=(255, 255, 255, 14), width=2)

    fb = lambda s: font(BOLD, s)
    fr = lambda s: font(REG, s)

    text_center(d, W / 2, 66, "W I K I D O C S   T E C H   B O O K", fr(26), CORAL)
    d.line([(120, 128), (880, 128)], fill=LINE, width=2)

    text_center(d, W / 2, 210, "Claude Code", fb(100), WHITE)
    text_center(d, W / 2, 335, "실전", fb(100), CORAL)

    text_center(d, W / 2, 510, "터미널에서 시작하는", fb(44), WHITE)
    text_center(d, W / 2, 576, "AI 코딩 실전서", fb(44), WHITE)

    rrect(d, [160, 690, 840, 758], 34, PANEL, outline=LINE, width=2)
    text_center(d, W / 2, 706, "일을 맡기고 검증하는 개발 방식", fb(32), WHITE)

    topics = [
        "CLAUDE.md와 슬래시 커맨드",
        "서브에이전트와 계획 모드",
        "hooks · MCP 연동 · 스킬",
        "컨텍스트와 장시간 작업 관리",
        "팀 도입과 CI/CD 연동",
    ]
    y = 810
    text_center(d, W / 2, y, "이 책에서 다루는 내용", fr(26), MUTED)
    y += 44
    for i, t in enumerate(topics):
        rrect(d, [170, y, 830, y + 46], 23, (20, 28, 54), outline=(60, 76, 120), width=1)
        d.ellipse([194, y + 11, 228, y + 45], fill=CORAL)
        fnum = fb(26)
        num = str(i + 1)
        bb = d.textbbox((0, 0), num, font=fnum)
        d.text((211 - (bb[2] - bb[0]) / 2 - bb[0], y + 13), num, font=fnum, fill=(255, 255, 255))
        d.text((244, y + 15), t, font=fr(24), fill=WHITE)
        y += 56

    d.line([(120, 1130), (880, 1130)], fill=LINE, width=2)
    text_center(d, W / 2, 1158, "저자  이준수", fr(30), MUTED)
    text_center(d, W / 2, 1202, "기준일  2026-10-09", fr(26), MUTED)

    img.save(os.path.join(ASSETS, "cover.png"))
    print("cover.png saved")


# ------------------------------------------------- 작업 흐름 1500x560
def make_session_flow():
    W, H = 1500, 560
    img = Image.new("RGB", (W, H), LIGHT_BG)
    d = ImageDraw.Draw(img)
    fb = lambda s: font(BOLD, s)
    fr = lambda s: font(REG, s)

    text_center(d, W / 2, 24, "Claude Code Working Loop", fb(40), INK)
    text_center(d, W / 2, 78, "지시 → 탐색 → 계획 → 실행 → 검증의 반복",
                fr(26), SUB)

    steps = [
        ("지시", "목표·제약\n검증 방법", CORAL),
        ("탐색", "파일 읽기\n구조 파악", BLUE),
        ("계획", "단계별 계획\n검토와 승인", TEAL),
        ("실행", "코드 수정\n명령 실행", (139, 92, 246)),
        ("검증", "테스트 실행\n사람 리뷰", (245, 158, 11)),
    ]
    x0, bw, gap = 40, 252, 30
    y0 = 170
    for i, (t, desc, color) in enumerate(steps):
        x = x0 + i * (bw + gap)
        rrect(d, [x, y0, x + bw, y0 + 210], 20, (255, 255, 255),
              outline=CARD_LINE, width=2)
        d.rectangle([x, y0, x + bw, y0 + 12], fill=color)
        text_center(d, x + bw / 2, y0 + 34, t, fb(32), INK)
        for j, line in enumerate(desc.split("\n")):
            text_center(d, x + bw / 2, y0 + 84 + j * 38, line, fr(24), SUB)
        if i < 4:
            arrow(d, x + bw + 5, y0 + 105, x + bw + gap - 5, y0 + 105,
                  fill=(148, 163, 184), width=5)

    text_center(d, W / 2, 450, "방향이 틀리면 Esc로 멈추고 바로잡는다",
                fr(26), SUB)
    img.save(os.path.join(ASSETS, "fig-session-flow.png"))
    print("fig-session-flow.png saved")


# ------------------------------------------------- 서브에이전트 1400x620
def make_subagents():
    W, H = 1400, 620
    img = Image.new("RGB", (W, H), LIGHT_BG)
    d = ImageDraw.Draw(img)
    fb = lambda s: font(BOLD, s)
    fr = lambda s: font(REG, s)

    text_center(d, W / 2, 24, "Subagents: Parallel Delegation", fb(40), INK)
    text_center(d, W / 2, 78, "독립적인 작업은 나누어 병렬로 처리한다",
                fr(26), SUB)

    rrect(d, [550, 150, 850, 280], 20, (30, 41, 59))
    text_center(d, 700, 172, "Main Session", fb(32), WHITE)
    text_center(d, 700, 216, "작업 분할과 결과 취합", fr(24), (203, 213, 225))

    subs = [
        (120, 380, "인증 모듈 분석", BLUE),
        (420, 380, "결제 모듈 분석", TEAL),
        (720, 380, "DB 모듈 분석", CORAL),
        (1020, 380, "API 모듈 분석", (139, 92, 246)),
    ]
    for x, y, t, color in subs:
        rrect(d, [x, y, x + 260, y + 120], 18, (255, 255, 255), outline=color, width=3)
        text_center(d, x + 130, y + 28, "Subagent", fr(22), SUB)
        text_center(d, x + 130, y + 58, t, fb(26), INK)
        arrow(d, 700, 285, x + 130, y - 5, fill=color, width=3)

    text_center(d, W / 2, 550, "각 서브에이전트는 자기 작업에만 집중, 메인은 결과만 받는다",
                fr(26), SUB)
    img.save(os.path.join(ASSETS, "fig-subagents.png"))
    print("fig-subagents.png saved")


# ------------------------------------------------- hooks 1400x560
def make_hooks():
    W, H = 1400, 560
    img = Image.new("RGB", (W, H), LIGHT_BG)
    d = ImageDraw.Draw(img)
    fb = lambda s: font(BOLD, s)
    fr = lambda s: font(REG, s)

    text_center(d, W / 2, 24, "Hooks: Automatic Checks", fb(40), INK)
    text_center(d, W / 2, 78, "특정 시점에 스크립트가 자동으로 실행된다",
                fr(26), SUB)

    hooks = [
        ("파일 수정 전", "검사 실행\n규칙 위반 차단", CORAL),
        ("파일 쓰기 후", "포매터 실행\n형식 자동 정리", TEAL),
        ("명령 실행 전", "위험 패턴 검사\n승인 요청", BLUE),
        ("세션 종료 시", "변경 요약\n알림 전송", (139, 92, 246)),
    ]
    x0, bw, gap = 60, 290, 30
    y0 = 170
    for i, (t, desc, color) in enumerate(hooks):
        x = x0 + i * (bw + gap)
        rrect(d, [x, y0, x + bw, y0 + 190], 20, (255, 255, 255),
              outline=CARD_LINE, width=2)
        d.rectangle([x, y0, x + bw, y0 + 12], fill=color)
        text_center(d, x + bw / 2, y0 + 34, t, fb(28), INK)
        for j, line in enumerate(desc.split("\n")):
            text_center(d, x + bw / 2, y0 + 80 + j * 36, line, fr(24), SUB)

    text_center(d, W / 2, 440, "꼭 필요한 것만 두고 스크립트는 단순하고 빠르게",
                fr(26), SUB)
    img.save(os.path.join(ASSETS, "fig-hooks.png"))
    print("fig-hooks.png saved")


# ------------------------------------------------- MCP 연동 1400x620
def make_mcp_cc():
    W, H = 1400, 620
    img = Image.new("RGB", (W, H), LIGHT_BG)
    d = ImageDraw.Draw(img)
    fb = lambda s: font(BOLD, s)
    fr = lambda s: font(REG, s)

    text_center(d, W / 2, 24, "Claude Code + MCP", fb(40), INK)
    text_center(d, W / 2, 78, "claude mcp add로 외부 도구를 연결한다",
                fr(26), SUB)

    rrect(d, [550, 170, 850, 320], 22, (30, 41, 59))
    text_center(d, 700, 196, "Claude Code", fb(34), WHITE)
    text_center(d, 700, 242, "필요할 때 도구를 골라 호출", fr(24), (203, 213, 225))

    servers = [
        (80, 400, "DB 서버", "데이터 조회", BLUE),
        (400, 400, "이슈 트래커", "티켓 조회", TEAL),
        (880, 400, "문서 서버", "사내 문서 검색", CORAL),
        (1080, 400, "클라우드", "리소스 관리", (139, 92, 246)),
    ]
    for x, y, t, desc, color in servers:
        rrect(d, [x, y, x + 240, y + 110], 18, (255, 255, 255), outline=color, width=3)
        text_center(d, x + 120, y + 18, t, fb(26), INK)
        text_center(d, x + 120, y + 56, desc, fr(22), SUB)
        arrow(d, 700, 325, x + 120, y - 5, fill=color, width=3)

    text_center(d, W / 2, 560, "읽기 전용부터 시작, 작업에 필요한 것만 연결한다",
                fr(26), SUB)
    img.save(os.path.join(ASSETS, "fig-mcp-cc.png"))
    print("fig-mcp-cc.png saved")


# ------------------------------------------------- 실전 프로젝트 1500x640
def make_project():
    W, H = 1500, 640
    img = Image.new("RGB", (W, H), LIGHT_BG)
    d = ImageDraw.Draw(img)
    fb = lambda s: font(BOLD, s)
    fr = lambda s: font(REG, s)

    text_center(d, W / 2, 24, "Codebase Adoption Project", fb(40), INK)
    text_center(d, W / 2, 78, "탐색 → 문서화 → 테스트 → 리팩토링 → 정리의 5단계",
                fr(26), SUB)

    steps = [
        ("1. 탐색·계획", "구조 파악\n계획 모드로 수립", CORAL),
        ("2. 문서화", "모듈 README\n사람이 검증", BLUE),
        ("3. 테스트", "테스트 작성\n직접 실행 확인", TEAL),
        ("4. 리팩토링", "계획 승인 후\n전체 테스트", (139, 92, 246)),
        ("5. 정리", "단계별 커밋\n전체 diff 리뷰", (245, 158, 11)),
    ]
    x0, bw, gap = 40, 252, 30
    y0 = 170
    for i, (t, desc, color) in enumerate(steps):
        x = x0 + i * (bw + gap)
        rrect(d, [x, y0, x + bw, y0 + 200], 20, (255, 255, 255),
              outline=CARD_LINE, width=2)
        d.rectangle([x, y0, x + bw, y0 + 12], fill=color)
        text_center(d, x + bw / 2, y0 + 34, t, fb(28), INK)
        for j, line in enumerate(desc.split("\n")):
            text_center(d, x + bw / 2, y0 + 80 + j * 36, line, fr(24), SUB)
        if i < 4:
            arrow(d, x + bw + 5, y0 + 100, x + bw + gap - 5, y0 + 100,
                  fill=(148, 163, 184), width=5)

    rrect(d, [40, 450, 1460, 570], 18, (30, 41, 59))
    text_center(d, 750, 470, "각 단계의 결과물은 사람이 검증한다", fb(28), CORAL)
    text_center(d, 750, 512, "과정에서 만든 CLAUDE.md · 커맨드 · 스킬은 팀의 자산으로 남는다",
                fr(24), (203, 213, 225))

    img.save(os.path.join(ASSETS, "fig-project.png"))
    print("fig-project.png saved")


if __name__ == "__main__":
    os.makedirs(ASSETS, exist_ok=True)
    make_cover()
    make_session_flow()
    make_subagents()
    make_hooks()
    make_mcp_cc()
    make_project()
