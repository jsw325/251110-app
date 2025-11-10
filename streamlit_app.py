import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


st.set_page_config(page_title="이차함수 그래프", layout="wide")

st.title("📈 이차함수 그래프 그리기")
st.write("기본 형태: y = a x² + b x + c — a, b, c 값을 바꿔 그래프를 확인하세요.")

with st.sidebar:
    st.header("파라미터")
    a = st.number_input("a (이차항 계수)", value=1.0, step=0.1, format="%.3f")
    b = st.number_input("b (일차항 계수)", value=0.0, step=0.1, format="%.3f")
    c = st.number_input("c (상수항)", value=0.0, step=0.1, format="%.3f")
    st.markdown("---")
    st.header("x 범위")
    x_min = st.number_input("x 최소값", value=-10.0, step=1.0, format="%.3f")
    x_max = st.number_input("x 최대값", value=10.0, step=1.0, format="%.3f")
    n_points = st.slider("샘플 수 (정밀도)", min_value=100, max_value=5000, value=400, step=100)
    st.markdown("---")
    show_vertex = st.checkbox("꼭짓점 표시", value=True)
    show_roots = st.checkbox("실근 표시(존재하면)", value=True)
    st.markdown("---")
    st.write("힌트: a가 0이면 1차함수입니다.")


def compute_roots(a, b, c):
    if a == 0:
        # linear bx + c = 0 -> x = -c/b if b != 0
        if b == 0:
            return []
        return [-c / b]
    D = b * b - 4 * a * c
    if D < 0:
        return []
    elif D == 0:
        return [(-b) / (2 * a)]
    else:
        sqrtD = np.sqrt(D)
        return [(-b - sqrtD) / (2 * a), (-b + sqrtD) / (2 * a)]


if x_min >= x_max:
    st.error("x 최소값은 x 최대값보다 작아야 합니다.")
else:
    x = np.linspace(x_min, x_max, n_points)
    if a == 0:
        y = b * x + c
        func_label = f"y = {b:.3f}x + {c:.3f}"
    else:
        y = a * x ** 2 + b * x + c
        func_label = f"y = {a:.3f}x² + {b:.3f}x + {c:.3f}"

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, y, label=func_label, color="#1f77b4")
    ax.axhline(0, color="black", linewidth=0.8)  # x축
    ax.axvline(0, color="black", linewidth=0.8)  # y축
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.set_title("이차함수 그래프 (가로: x축, 세로: y축)")

    # 꼭짓점
    if a != 0 and show_vertex:
        xv = -b / (2 * a)
        yv = a * xv ** 2 + b * xv + c
        ax.scatter([xv], [yv], color="red", zorder=5)
        ax.annotate(f"꼭짓점 ({xv:.3f}, {yv:.3f})", xy=(xv, yv), xytext=(10, -15), textcoords="offset points", color="red")
        st.write(f"꼭짓점: x = {xv:.3f}, y = {yv:.3f}")

    # 실근
    if show_roots:
        roots = compute_roots(a, b, c)
        if len(roots) == 0:
            st.write("실근: 없음")
        else:
            roots_in_range = [r for r in roots if r >= x_min - 1e-8 and r <= x_max + 1e-8]
            for r in roots:
                yr = a * r ** 2 + b * r + c if a != 0 else b * r + c
                ax.scatter([r], [yr], color="green", zorder=6)
                ax.annotate(f"root {r:.3f}", xy=(r, yr), xytext=(5, 5), textcoords="offset points", color="green")
            st.write("실근:", ", ".join([f"{r:.3f}" for r in roots]) if roots else "없음")

    ax.legend()
    st.pyplot(fig)
