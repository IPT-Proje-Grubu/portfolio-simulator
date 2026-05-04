"""LoginDialog — polished registration / login screen matching the app's dark palette."""

from __future__ import annotations

import uuid
from typing import Any

from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtGui import QFont, QLinearGradient, QColor, QPainter, QPainterPath
from PyQt6.QtWidgets import (
    QDialog,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from src.db.database import Database, UserRow
from src.ui.i18n import LANG_EN, LANG_TR, apply_language_to_widget, lang_manager

# ── palette (matches main_window.py) ─────────────────────────────────────────
_BG      = "#0b0f1a"
_SURF    = "#111827"
_SURF2   = "#1a2235"
_BORDER  = "#1e2d45"
_ACCENT  = "#2563eb"
_ACCH    = "#1d4ed8"
_GREEN   = "#10b981"
_RED     = "#ef4444"
_AMBER   = "#f59e0b"
_TEXT    = "#e2e8f0"
_TEXT2   = "#94a3b8"
_TEXT3   = "#64748b"

# ── helper ────────────────────────────────────────────────────────────────────

def _input(placeholder: str, *, echo_mode: QLineEdit.EchoMode | None = None) -> QLineEdit:
    le = QLineEdit()
    le.setPlaceholderText(placeholder)
    le.setFixedHeight(46)
    if echo_mode is not None:
        le.setEchoMode(echo_mode)
    le.setStyleSheet(f"""
        QLineEdit {{
            background: {_SURF2};
            color: {_TEXT};
            border: 1.5px solid {_BORDER};
            border-radius: 10px;
            padding: 0 16px;
            font-size: 14px;
            selection-background-color: {_ACCENT};
        }}
        QLineEdit:focus {{
            border-color: {_ACCENT};
            background: #0f172a;
        }}
        QLineEdit::placeholder {{
            color: {_TEXT3};
        }}
    """)
    return le


def _action_btn(text: str) -> QPushButton:
    b = QPushButton(text)
    b.setFixedHeight(48)
    b.setCursor(Qt.CursorShape.PointingHandCursor)
    b.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
    b.setStyleSheet(f"""
        QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {_ACCENT}, stop:1 #3b82f6);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 14px;
            font-weight: 700;
            letter-spacing: 0.5px;
        }}
        QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {_ACCH}, stop:1 #2563eb);
        }}
        QPushButton:pressed {{
            background: #1e40af;
        }}
    """)
    return b


def _link_btn(text: str) -> QPushButton:
    b = QPushButton(text)
    b.setCursor(Qt.CursorShape.PointingHandCursor)
    b.setFlat(True)
    b.setStyleSheet(f"""
        QPushButton {{
            color: {_ACCENT};
            background: transparent;
            border: none;
            font-size: 13px;
            font-weight: 600;
            text-decoration: underline;
            padding: 4px 0;
        }}
        QPushButton:hover {{
            color: #60a5fa;
        }}
    """)
    return b


def _lang_btn(text: str) -> QPushButton:
    b = QPushButton(text)
    b.setFixedHeight(34)
    b.setFixedWidth(64)
    b.setCursor(Qt.CursorShape.PointingHandCursor)
    b.setCheckable(True)
    b.setStyleSheet(f"""
        QPushButton {{
            background: {_SURF};
            color: {_TEXT3};
            border: 1px solid {_BORDER};
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
        }}
        QPushButton:hover {{
            background: {_SURF2};
            color: {_TEXT2};
        }}
        QPushButton:checked {{
            background: {_ACCENT};
            color: white;
            border: none;
            font-weight: 700;
        }}
    """)
    return b


# ══════════════════════════════════════════════════════════════════════════════
#  LoginDialog
# ══════════════════════════════════════════════════════════════════════════════

class LoginDialog(QDialog):
    """Modal dialog for user registration / login.

    On successful authentication, ``self.user_row`` contains a ``UserRow``
    and ``self.session_id`` holds a fresh UUID for the session.
    """

    def __init__(self, db: Database, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._db = db
        self.user_row: UserRow | None = None
        self.session_id: str = ""

        self.setWindowTitle(lang_manager.tr("PortfolioSim — Giriş"))
        self.setFixedSize(480, 620)
        self.setModal(True)
        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._build()
        lang_manager.subscribe(lambda _lang: self._apply_language())
        self._apply_language()

    # ── paint rounded container ───────────────────────────────────────────────

    def paintEvent(self, event: Any) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        # rounded rect background
        path = QPainterPath()
        path.addRoundedRect(0.0, 0.0, float(self.width()), float(self.height()), 18.0, 18.0)
        p.setClipPath(path)

        # subtle gradient background
        grad = QLinearGradient(0, 0, 0, self.height())
        grad.setColorAt(0, QColor("#0d1325"))
        grad.setColorAt(1, QColor(_BG))
        p.fillPath(path, grad)

        # thin border
        p.setPen(QColor(_BORDER))
        p.drawPath(path)
        p.end()

    # ── drag support (frameless) ──────────────────────────────────────────────

    def mousePressEvent(self, e: Any) -> None:
        if e.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()
            e.accept()

    def mouseMoveEvent(self, e: Any) -> None:
        if hasattr(self, "_drag_pos") and e.buttons() & Qt.MouseButton.LeftButton:
            self.move(e.globalPosition().toPoint() - self._drag_pos)
            e.accept()

    # ── build ─────────────────────────────────────────────────────────────────

    def _build(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(36, 16, 36, 30)
        root.setSpacing(0)

        # ── close button ──────────────────────────────────────────────────────
        close_row = QHBoxLayout()
        close_row.setContentsMargins(0, 0, 0, 0)
        close_row.addStretch()
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(32, 32)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {_TEXT3};
                border: none;
                border-radius: 16px;
                font-size: 16px;
                font-weight: 700;
            }}
            QPushButton:hover {{
                background: {_RED};
                color: white;
            }}
        """)
        close_btn.clicked.connect(self.reject)
        close_row.addWidget(close_btn)
        root.addLayout(close_row)

        # ── header ────────────────────────────────────────────────────────────
        logo = QLabel("◆")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet(f"""
            color: {_ACCENT};
            font-size: 36px;
            font-weight: 900;
            padding-bottom: 2px;
        """)
        root.addWidget(logo)

        title = QLabel("PortfolioSim")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"""
            color: {_TEXT};
            font-size: 24px;
            font-weight: 800;
            letter-spacing: 1px;
        """)
        root.addWidget(title)

        subtitle = QLabel("Yatırım simülasyon platformu")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(f"color: {_TEXT3}; font-size: 12px; margin-bottom: 8px;")
        root.addWidget(subtitle)
        root.addSpacing(24)

        lang_row = QHBoxLayout()
        lang_row.addStretch()
        self._btn_lang_tr = _lang_btn("TR")
        self._btn_lang_en = _lang_btn("EN")
        self._btn_lang_tr.clicked.connect(lambda: self._set_lang(LANG_TR))
        self._btn_lang_en.clicked.connect(lambda: self._set_lang(LANG_EN))
        lang_row.addWidget(self._btn_lang_tr)
        lang_row.addWidget(self._btn_lang_en)
        lang_row.addStretch()
        root.addLayout(lang_row)
        root.addSpacing(10)

        # ── tab switcher ──────────────────────────────────────────────────────
        tab_row = QHBoxLayout()
        tab_row.setSpacing(0)
        self._tab_login = QPushButton("Giriş Yap")
        self._tab_register = QPushButton("Kayıt Ol")
        for btn in (self._tab_login, self._tab_register):
            btn.setFixedHeight(40)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setCheckable(True)
        self._tab_login.setChecked(True)
        self._tab_login.clicked.connect(lambda: self._switch_tab(0))
        self._tab_register.clicked.connect(lambda: self._switch_tab(1))
        tab_row.addWidget(self._tab_login, 1)
        tab_row.addWidget(self._tab_register, 1)
        self._apply_tab_styles()
        root.addLayout(tab_row)
        root.addSpacing(20)

        # ── stacked forms ─────────────────────────────────────────────────────
        self._stack = QStackedWidget()

        # login form
        login_w = QWidget()
        login_vl = QVBoxLayout(login_w)
        login_vl.setContentsMargins(0, 0, 0, 0)
        login_vl.setSpacing(14)

        self._l_user = _input("Kullanıcı adı")
        self._l_pass = _input("Şifre", echo_mode=QLineEdit.EchoMode.Password)
        self._l_btn  = _action_btn("Giriş Yap  →")
        self._l_err  = QLabel("")
        self._l_err.setWordWrap(True)
        self._l_err.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._l_err.setStyleSheet(f"color: {_RED}; font-size: 12px; min-height: 18px;")

        login_vl.addWidget(self._l_user)
        login_vl.addWidget(self._l_pass)
        login_vl.addSpacing(4)
        login_vl.addWidget(self._l_err)
        login_vl.addWidget(self._l_btn)
        login_vl.addStretch()

        lnk = _link_btn("Hesabın yok mu?  Kayıt ol →")
        lnk.clicked.connect(lambda: self._switch_tab(1))
        login_vl.addWidget(lnk, alignment=Qt.AlignmentFlag.AlignCenter)

        self._stack.addWidget(login_w)

        # register form
        reg_w = QWidget()
        reg_vl = QVBoxLayout(reg_w)
        reg_vl.setContentsMargins(0, 0, 0, 0)
        reg_vl.setSpacing(14)

        self._r_user  = _input("Kullanıcı adı (en az 3 karakter)")
        self._r_pass  = _input("Şifre (en az 4 karakter)", echo_mode=QLineEdit.EchoMode.Password)
        self._r_pass2 = _input("Şifre tekrar", echo_mode=QLineEdit.EchoMode.Password)
        self._r_btn   = _action_btn("Kayıt Ol  ✓")
        self._r_err   = QLabel("")
        self._r_err.setWordWrap(True)
        self._r_err.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._r_err.setStyleSheet(f"color: {_RED}; font-size: 12px; min-height: 18px;")

        reg_vl.addWidget(self._r_user)
        reg_vl.addWidget(self._r_pass)
        reg_vl.addWidget(self._r_pass2)
        reg_vl.addSpacing(4)
        reg_vl.addWidget(self._r_err)
        reg_vl.addWidget(self._r_btn)
        reg_vl.addStretch()

        lnk2 = _link_btn("Zaten hesabın var mı?  Giriş yap →")
        lnk2.clicked.connect(lambda: self._switch_tab(0))
        reg_vl.addWidget(lnk2, alignment=Qt.AlignmentFlag.AlignCenter)

        self._stack.addWidget(reg_w)

        root.addWidget(self._stack, 1)
        root.addSpacing(12)

        # ── footer ────────────────────────────────────────────────────────────
        footer = QLabel("🔒  Verileriniz yalnızca yerel olarak saklanır")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet(f"color: {_TEXT3}; font-size: 11px;")
        root.addWidget(footer)
        self._subtitle = subtitle
        self._link_to_register = lnk
        self._link_to_login = lnk2
        self._footer = footer

        # ── connect ───────────────────────────────────────────────────────────
        self._l_btn.clicked.connect(self._do_login)
        self._r_btn.clicked.connect(self._do_register)

        # Enter key submits
        self._l_pass.returnPressed.connect(self._do_login)
        self._r_pass2.returnPressed.connect(self._do_register)

    def _set_lang(self, lang: str) -> None:
        lang_manager.set_language(lang)

    def _apply_language(self) -> None:
        tr = lang_manager.tr
        self.setWindowTitle(tr("PortfolioSim — Giriş"))
        self._subtitle.setText(tr("Yatırım simülasyon platformu"))
        self._tab_login.setText(tr("Giriş Yap"))
        self._tab_register.setText(tr("Kayıt Ol"))
        self._l_user.setPlaceholderText(tr("Kullanıcı adı"))
        self._l_pass.setPlaceholderText(tr("Şifre"))
        self._l_btn.setText(tr("Giriş Yap  →"))
        self._r_user.setPlaceholderText(tr("Kullanıcı adı (en az 3 karakter)"))
        self._r_pass.setPlaceholderText(tr("Şifre (en az 4 karakter)"))
        self._r_pass2.setPlaceholderText(tr("Şifre tekrar"))
        self._r_btn.setText(tr("Kayıt Ol  ✓"))
        self._link_to_register.setText(tr("Hesabın yok mu?  Kayıt ol →"))
        self._link_to_login.setText(tr("Zaten hesabın var mı?  Giriş yap →"))
        self._footer.setText(tr("🔒  Verileriniz yalnızca yerel olarak saklanır"))
        self._btn_lang_tr.setChecked(lang_manager.language == LANG_TR)
        self._btn_lang_en.setChecked(lang_manager.language == LANG_EN)
        apply_language_to_widget(self, lang_manager.language)

    # ── tab switching ─────────────────────────────────────────────────────────

    def _switch_tab(self, index: int) -> None:
        self._stack.setCurrentIndex(index)
        self._tab_login.setChecked(index == 0)
        self._tab_register.setChecked(index == 1)
        self._apply_tab_styles()
        # clear errors
        self._l_err.setText("")
        self._r_err.setText("")

    def _apply_tab_styles(self) -> None:
        active_ss = f"""
            QPushButton {{
                background: {_ACCENT};
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 700;
            }}
        """
        inactive_ss = f"""
            QPushButton {{
                background: {_SURF};
                color: {_TEXT3};
                border: 1px solid {_BORDER};
                border-radius: 8px;
                font-size: 13px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background: {_SURF2};
                color: {_TEXT2};
            }}
        """
        self._tab_login.setStyleSheet(active_ss if self._tab_login.isChecked() else inactive_ss)
        self._tab_register.setStyleSheet(active_ss if self._tab_register.isChecked() else inactive_ss)

    # ── actions ───────────────────────────────────────────────────────────────

    def _show_error(self, label: QLabel, msg: str) -> None:
        label.setText(msg)
        label.setStyleSheet(f"color: {_RED}; font-size: 12px; min-height: 18px;")

    def _show_success(self, label: QLabel, msg: str) -> None:
        label.setText(msg)
        label.setStyleSheet(f"color: {_GREEN}; font-size: 12px; min-height: 18px;")

    def _do_login(self) -> None:
        username = self._l_user.text().strip()
        password = self._l_pass.text()

        if not username or not password:
            self._show_error(self._l_err, lang_manager.db_error("Lütfen kullanıcı adı ve şifre girin."))
            return

        result = self._db.verify_login(username, password)
        if isinstance(result, str):
            self._show_error(self._l_err, lang_manager.db_error(result))
            return

        # success
        self.user_row = result
        self.session_id = uuid.uuid4().hex
        self._db.start_session(result.id, self.session_id)
        if lang_manager.language == LANG_EN:
            self._show_success(self._l_err, f"Welcome, {result.username}!")
        else:
            self._show_success(self._l_err, f"Hoş geldin, {result.username}!")
        QTimer.singleShot(600, self.accept)

    def _do_register(self) -> None:
        username = self._r_user.text().strip()
        password = self._r_pass.text()
        password2 = self._r_pass2.text()

        if not username or not password:
            self._show_error(self._r_err, lang_manager.db_error("Lütfen tüm alanları doldurun."))
            return
        if password != password2:
            self._show_error(self._r_err, lang_manager.db_error("Şifreler eşleşmiyor."))
            return

        result = self._db.register_user(username, password)
        if isinstance(result, str):
            self._show_error(self._r_err, lang_manager.db_error(result))
            return

        # auto-login after registration
        self.user_row = result
        self.session_id = uuid.uuid4().hex
        self._db.start_session(result.id, self.session_id)
        if lang_manager.language == LANG_EN:
            self._show_success(self._r_err, f"Registration successful! Welcome, {result.username}!")
        else:
            self._show_success(self._r_err, f"Kayıt başarılı!  Hoş geldin, {result.username}!")
        QTimer.singleShot(800, self.accept)
