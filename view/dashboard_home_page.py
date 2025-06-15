import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QFrame, QGridLayout, QScrollArea, QComboBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon, QColor, QLinearGradient, QBrush
import pyqtgraph as pg
from datetime import datetime, timedelta

from .base_dashboard_page import BaseDashboardPage

class ModernKpiCard(QFrame):
    def __init__(self, title, icon_path=None, accent_color="#6366f1", parent=None):
        super().__init__(parent)
        self.accent_color = accent_color
        self.setFrameShape(QFrame.NoFrame)
        self.setObjectName("modernKpiCard")
        
        self.setStyleSheet(f"""
            #modernKpiCard {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.95), 
                    stop:1 rgba(248, 250, 252, 0.90));
                border: 1px solid rgba(59, 130, 246, 0.15);
                border-radius: 20px;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px rgba(59, 130, 246, 0.08);
            }}
            #modernKpiCard:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 1), 
                    stop:1 rgba(240, 249, 255, 0.95));
                border: 1px solid {self.accent_color}60;
                transform: translateY(-2px);
                box-shadow: 0 12px 40px rgba(59, 130, 246, 0.15);
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)
        
        header_layout = QHBoxLayout()
        header_layout.setSpacing(16)
        
        if icon_path and os.path.exists(icon_path):
            icon_container = QFrame()
            icon_container.setFixedSize(56, 56)
            icon_container.setStyleSheet(f"""
                border-radius: 16px;
                box-shadow: 0 4px 16px {self.accent_color}40;
            """)
            
            icon_layout = QVBoxLayout(icon_container)
            icon_label = QLabel()
            icon_label.setPixmap(QIcon(icon_path).pixmap(28, 28))
            icon_label.setAlignment(Qt.AlignCenter)
            icon_layout.addWidget(icon_label)
            header_layout.addWidget(icon_container)

        title_container = QVBoxLayout()
        self.title_label = QLabel(title)
        self.title_label.setFont(QFont("Segoe UI Variable", 14, QFont.DemiBold))
        self.title_label.setStyleSheet("color: #475569; margin: 0px; border: none; background: transparent;")
        
        self.subtitle_label = QLabel("Current period")
        self.subtitle_label.setFont(QFont("Segoe UI Variable", 11))
        self.subtitle_label.setStyleSheet("color: #94a3b8; margin: 0px; border: none; background: transparent;")
        
        title_container.addWidget(self.title_label)
        title_container.addWidget(self.subtitle_label)
        
        header_layout.addLayout(title_container)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        self.value_label = QLabel("Loading...")
        self.value_label.setFont(QFont("Segoe UI Variable", 36, QFont.Bold))
        self.value_label.setStyleSheet(f"""
            color: #0f172a; 
            margin-top: 12px; 
            border: none; 
            background: transparent;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        """)
        
        layout.addWidget(self.value_label)
        
    def set_value(self, value_text):
        self.value_label.setText(value_text)
    
    def _darken_color(self, color_hex):
        color = QColor(color_hex)
        h, s, l, a = color.getHsl()
        darker = QColor.fromHsl(h, min(255, s+20), max(0, l-30), a)
        return darker.name()

class DashboardHomePage(BaseDashboardPage):
    def __init__(self, user_id, product_processor, user_processor, data_changed_signal, parent=None):
        super().__init__("Dashboard Overview", parent=parent)
        self.user_id = user_id
        self.db_manager = product_processor.db_manager
        data_changed_signal.connect(self.load_page_data)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: #F8F9FA;
                width: 12px;
                border-radius: 6px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #CED4DA;
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #ADB5BD;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        scroll_content_widget = QWidget()
        scroll_area.setWidget(scroll_content_widget)

        main_content_layout = QVBoxLayout(scroll_content_widget)
        main_content_layout.setContentsMargins(32, 24, 32, 32)
        main_content_layout.setSpacing(32)

        header_layout = self._create_modern_header()
        main_content_layout.addLayout(header_layout)

        filter_layout, self.date_display_label = self._create_modern_filter_bar()
        main_content_layout.addLayout(filter_layout)

        kpi_layout = QHBoxLayout()
        kpi_layout.setSpacing(24)
        
        self.kpi_revenue = ModernKpiCard("Total Revenue", "assets/icons/revenue.png", "#10b981")
        self.kpi_items_sold = ModernKpiCard("Items Sold", "assets/icons/sales.png", "#3b82f6") 
        self.kpi_stock = ModernKpiCard("Stock Units", "assets/icons/stock.png", "#8b5cf6")
        
        kpi_layout.addWidget(self.kpi_revenue)
        kpi_layout.addWidget(self.kpi_items_sold)
        kpi_layout.addWidget(self.kpi_stock)
        
        main_content_layout.addLayout(kpi_layout)
        
        grid_layout = QGridLayout()
        grid_layout.setSpacing(24)
        
        grid_layout.addWidget(self._create_modern_chart_panel(), 0, 0, 1, 3)
        grid_layout.addWidget(self._create_modern_attention_panel(), 1, 0)
        grid_layout.addWidget(self._create_modern_top_products_panel(), 1, 1)
        grid_layout.addWidget(self._create_modern_recent_activity_panel(), 1, 2)

        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 1)
        grid_layout.setColumnStretch(2, 1)
        
        main_content_layout.addLayout(grid_layout)

        self.content_layout.addWidget(scroll_area)

    def _create_modern_header(self):
        header_layout = QVBoxLayout()
        header_layout.setSpacing(8)
        
        welcome_label = QLabel("Dashboard Overview")
        welcome_label.setFont(QFont("Segoe UI Variable", 28, QFont.Bold))
        welcome_label.setStyleSheet("""
            color: #0f172a;
            background: transparent;
            margin: 0;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        """)
        
        subtitle_label = QLabel("Monitor your business performance and key metrics")
        subtitle_label.setFont(QFont("Segoe UI Variable", 14))
        subtitle_label.setStyleSheet("color: #64748b; background: transparent; margin: 0;")
        
        header_layout.addWidget(welcome_label)
        header_layout.addWidget(subtitle_label)
        
        return header_layout

    def load_page_data(self):
        super().load_page_data()
        self.date_filter_combo.setCurrentIndex(1)
        self.refresh_dashboard()

    def _create_modern_filter_bar(self):
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(20)
        
        date_display_label = QLabel()
        date_display_label.setFont(QFont("Segoe UI Variable", 13, QFont.DemiBold))
        date_display_label.setStyleSheet("""
            color: #1e40af; 
            background: transparent;
            padding: 12px 20px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(239, 246, 255, 0.8),
                stop:1 rgba(219, 234, 254, 0.7));
            border: 1px solid rgba(59, 130, 246, 0.2);
            border-radius: 16px;
            backdrop-filter: blur(10px);
        """)
        filter_layout.addWidget(date_display_label)
        filter_layout.addStretch()
        
        filter_container = QFrame()
        filter_container.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(255, 255, 255, 0.9),
                stop:1 rgba(240, 249, 255, 0.8));
            border: 1px solid rgba(59, 130, 246, 0.2);
            border-radius: 16px;
            padding: 8px;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 16px rgba(59, 130, 246, 0.08);
        """)
        filter_inner_layout = QHBoxLayout(filter_container)
        filter_inner_layout.setContentsMargins(12, 8, 12, 8)
        
        self.date_filter_combo = QComboBox()
        self.date_filter_combo.setStyleSheet("""
            QComboBox {
                border: none;
                padding: 8px 16px;
                font-family: 'Segoe UI Variable';
                font-size: 13px;
                font-weight: 500;
                color: #334155;
                background: transparent;
                min-width: 120px;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 8px;
                selection-background-color: #f1f5f9;
            }
        """)
        self.date_filter_combo.addItem("This Week", 7)
        self.date_filter_combo.addItem("Last 30 Days", 30)
        self.date_filter_combo.addItem("Last 90 Days", 90)
        self.date_filter_combo.currentIndexChanged.connect(self.refresh_dashboard)
        
        filter_inner_layout.addWidget(self.date_filter_combo)
        filter_layout.addWidget(filter_container)
        
        return filter_layout, date_display_label

    def refresh_dashboard(self):
        days = self.date_filter_combo.currentData()
        if not days: return

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days-1)

        start_str = start_date.strftime('%b %d, %Y')
        end_str = end_date.strftime('%b %d, %Y')
        self.date_display_label.setText(f"{start_str} - {end_str}")

        self.kpi_revenue.subtitle_label.setText(f"Last {days} days")
        self.kpi_items_sold.subtitle_label.setText(f"Last {days} days")
        self.kpi_stock.subtitle_label.setText("Current inventory")

        self._load_kpi_data(start_date, end_date)
        self._load_chart_data(days)
        self._load_top_products(start_date, end_date)
        self._load_attention_items()
        self._load_recent_activity()

    def _load_kpi_data(self, start_date, end_date):
        kpi_data = self.db_manager.get_kpi_data(self.user_id, start_date, end_date)
        self.kpi_revenue.set_value(f"${kpi_data.get('revenue', 0):,.2f}")
        self.kpi_items_sold.set_value(f"{kpi_data.get('items_sold', 0):,}")
        self.kpi_stock.set_value(f"{kpi_data.get('total_stock', 0):,}")

    def _create_panel_base(self, height=None):
        panel = QFrame()
        panel.setObjectName("modernPanel")
        if height:
            panel.setMinimumHeight(height)
        panel.setStyleSheet("""
            #modernPanel {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.95), 
                    stop:1 rgba(248, 250, 252, 0.90));
                border: 1px solid rgba(59, 130, 246, 0.15);
                border-radius: 20px;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px rgba(59, 130, 246, 0.08);
            }
        """)
        return panel

    def _create_modern_chart_panel(self):
        panel = self._create_panel_base(400)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(20)
        
        header_layout = QHBoxLayout()
        self.chart_title = QLabel("Revenue Analytics")
        self.chart_title.setFont(QFont("Segoe UI Variable", 18, QFont.Bold))
        self.chart_title.setStyleSheet("color: #0f172a; border: none; background: transparent;")
        header_layout.addWidget(self.chart_title)
        header_layout.addStretch()
        
        chart_subtitle = QLabel("Daily performance overview")
        chart_subtitle.setFont(QFont("Segoe UI Variable", 12))
        chart_subtitle.setStyleSheet("color: #64748b; border: none; background: transparent;")
        header_layout.addWidget(chart_subtitle)
        
        layout.addLayout(header_layout)
        
        pg.setConfigOption('background', None)
        pg.setConfigOption('foreground', '#334155')
        self.chart_widget = pg.PlotWidget()
        self.chart_widget.setStyleSheet("border: none; background: transparent;")
        self.chart_widget.showGrid(x=True, y=True, alpha=0.15)
        self.chart_widget.getAxis('left').setLabel('Revenue ($)', color='#64748b')
        self.chart_widget.getAxis('bottom').setLabel('Date', color='#64748b')
        
        for axis in ['left', 'bottom']:
            ax = self.chart_widget.getAxis(axis)
            ax.setTextPen('#64748b')
            ax.setPen(color='#cbd5e1', width=1)
        
        self.bar_chart = None
        layout.addWidget(self.chart_widget)
        return panel

    def _load_chart_data(self, days):
        chart_data = self.db_manager.get_daily_sales_for_chart(self.user_id, days)
        dates = list(chart_data.keys())
        revenues = list(chart_data.values())
        x_ticks = [datetime.combine(d, datetime.min.time()).timestamp() for d in dates]
        
        if self.bar_chart:
            self.chart_widget.removeItem(self.bar_chart)
        
        gradient = QLinearGradient(0, 0, 0, 1)
        gradient.setCoordinateMode(QLinearGradient.ObjectBoundingMode)
        gradient.setColorAt(0, QColor("#6366f1"))
        gradient.setColorAt(1, QColor("#4f46e5"))
        brush = QBrush(gradient)
        
        self.bar_chart = pg.BarGraphItem(
            x=x_ticks, 
            height=revenues, 
            width=0.6 * 86400, 
            brush=brush, 
            pen=pg.mkPen(color='#4338ca', width=2)
        )
        self.chart_widget.addItem(self.bar_chart)
        
        axis = self.chart_widget.getAxis('bottom')
        ticks = [(datetime.combine(d, datetime.min.time()).timestamp(), d.strftime('%m/%d')) 
                for d in dates if len(dates) < 15 or d.day % 5 == 0 or d.day == 1]
        axis.setTicks([ticks])

    def _create_modern_attention_panel(self):
        panel = self._create_panel_base(300)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)
        
        title = QLabel("Attention Required")
        title.setFont(QFont("Segoe UI Variable", 16, QFont.Bold))
        title.setStyleSheet("color: #0f172a; border: none; background: transparent;")
        layout.addWidget(title)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(59, 130, 246, 0.1),
                    stop:1 rgba(147, 197, 253, 0.1));
                width: 6px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6,
                    stop:1 #60a5fa);
                border-radius: 3px;
                min-height: 15px;
            }
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2563eb,
                    stop:1 #3b82f6);
            }
        """)
        
        content_widget = QWidget()
        self.attention_layout = QVBoxLayout(content_widget)
        self.attention_layout.setAlignment(Qt.AlignTop)
        self.attention_layout.setSpacing(8)
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
        
        return panel

    def _load_attention_items(self):
        while self.attention_layout.count():
            child = self.attention_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        attention_data = self.db_manager.get_attention_items(self.user_id)
        if not attention_data['low_stock']:
            success_label = QLabel("All items are well stocked!")
            success_label.setStyleSheet("""
                color: #059669;
                font-weight: 500;
                padding: 12px;
                background: rgba(16, 185, 129, 0.1);
                border-radius: 8px;
                border: 1px solid rgba(16, 185, 129, 0.2);
            """)
            self.attention_layout.addWidget(success_label)
        else:
            for _, name, qty in attention_data['low_stock']:
                item_widget = QFrame()
                item_widget.setStyleSheet("""
                    background: rgba(245, 101, 101, 0.1);
                    border: 1px solid rgba(245, 101, 101, 0.2);
                    border-radius: 8px;
                    padding: 8px;
                """)
                item_layout = QVBoxLayout(item_widget)
                item_layout.setContentsMargins(12, 8, 12, 8)
                
                item_label = QLabel(f"{name}")
                item_label.setFont(QFont("Segoe UI Variable", 12, QFont.DemiBold))
                item_label.setStyleSheet("color: #dc2626; background: transparent; border: none;")
                
                qty_label = QLabel(f"Only {qty} units remaining")
                qty_label.setFont(QFont("Segoe UI Variable", 10))
                qty_label.setStyleSheet("color: #991b1b; background: transparent; border: none;")
                
                item_layout.addWidget(item_label)
                item_layout.addWidget(qty_label)
                self.attention_layout.addWidget(item_widget)
        
        self.attention_layout.addStretch()

    def _create_modern_top_products_panel(self):
        panel = self._create_panel_base(300)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)
        
        self.top_products_title = QLabel("Top Performers")
        self.top_products_title.setFont(QFont("Segoe UI Variable", 16, QFont.Bold))
        self.top_products_title.setStyleSheet("color: #0f172a; border: none; background: transparent;")
        layout.addWidget(self.top_products_title)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(59, 130, 246, 0.1),
                    stop:1 rgba(147, 197, 253, 0.1));
                width: 6px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6,
                    stop:1 #60a5fa);
                border-radius: 3px;
                min-height: 15px;
            }
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2563eb,
                    stop:1 #3b82f6);
            }
        """)
        
        content_widget = QWidget()
        self.top_products_layout = QVBoxLayout(content_widget)
        self.top_products_layout.setAlignment(Qt.AlignTop)
        self.top_products_layout.setSpacing(8)
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
        
        return panel

    def _load_top_products(self, start_date, end_date):
        days = (end_date - start_date).days + 1
        self.top_products_title.setText(f"Top Performers ({days} days)")
        
        while self.top_products_layout.count():
            child = self.top_products_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        top_products = self.db_manager.get_top_products(self.user_id, start_date, end_date)
        if not top_products:
            no_data_label = QLabel(f"No sales data available for the last {days} days")
            no_data_label.setStyleSheet("""
                color: #64748b;
                font-style: italic;
                padding: 16px;
                background: rgba(148, 163, 184, 0.1);
                border-radius: 8px;
                text-align: center;
            """)
            self.top_products_layout.addWidget(no_data_label)
        else:
            for i, (name, revenue) in enumerate(top_products):
                rank_colors = ["#f59e0b", "#6b7280", "#cd7f32"]  
                rank_color = rank_colors[i] if i < 3 else "#64748b"
                
                item_widget = QFrame()
                item_widget.setStyleSheet(f"""
                    background: rgba(255, 255, 255, 0.5);
                    border: 1px solid rgba(0, 0, 0, 0.1);
                    border-left: 4px solid {rank_color};
                    border-radius: 8px;
                    padding: 4px;
                """)
                
                item_layout = QVBoxLayout(item_widget)
                item_layout.setContentsMargins(12, 8, 12, 8)
                
                name_label = QLabel(f"#{i+1} {name}")
                name_label.setFont(QFont("Segoe UI Variable", 12, QFont.DemiBold))
                name_label.setStyleSheet("color: #0f172a; background: transparent; border: none;")
                
                revenue_label = QLabel(f"${revenue:,.2f}")
                revenue_label.setFont(QFont("Segoe UI Variable", 11, QFont.Medium))
                revenue_label.setStyleSheet(f"color: {rank_color}; background: transparent; border: none;")
                
                item_layout.addWidget(name_label)
                item_layout.addWidget(revenue_label)
                self.top_products_layout.addWidget(item_widget)
        
        self.top_products_layout.addStretch()

    def _create_modern_recent_activity_panel(self):
        panel = self._create_panel_base(300)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)
        
        title = QLabel("Recent Activity")
        title.setFont(QFont("Segoe UI Variable", 16, QFont.Bold))
        title.setStyleSheet("color: #0f172a; border: none; background: transparent;")
        layout.addWidget(title)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(59, 130, 246, 0.1),
                    stop:1 rgba(147, 197, 253, 0.1));
                width: 6px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6,
                    stop:1 #60a5fa);
                border-radius: 3px;
                min-height: 15px;
            }
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2563eb,
                    stop:1 #3b82f6);
            }
        """)
        
        content_widget = QWidget()
        self.recent_activity_layout = QVBoxLayout(content_widget)
        self.recent_activity_layout.setAlignment(Qt.AlignTop)
        self.recent_activity_layout.setSpacing(8)
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
        
        return panel

    def _load_recent_activity(self):
        while self.recent_activity_layout.count():
            child = self.recent_activity_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        recent_activity = self.db_manager.get_recent_activity(self.user_id)
        if not recent_activity:
            no_activity_label = QLabel("No recent activity to display")
            no_activity_label.setStyleSheet("""
                color: #64748b;
                font-style: italic;
                padding: 16px;
                background: rgba(148, 163, 184, 0.1);
                border-radius: 8px;
                text-align: center;
            """)
            self.recent_activity_layout.addWidget(no_activity_label)
        else:
            for act_type, desc, date in recent_activity:
                date_str = datetime.fromisoformat(date).strftime('%b %d, %H:%M')
                
                activity_widget = QFrame()
                activity_widget.setStyleSheet("""
                    background: rgba(255, 255, 255, 0.5);
                    border: 1px solid rgba(0, 0, 0, 0.08);
                    border-radius: 8px;
                    padding: 4px;
                """)
                
                activity_layout = QVBoxLayout(activity_widget)
                activity_layout.setContentsMargins(12, 8, 12, 8)
                activity_layout.setSpacing(4)
                                
                type_label = QLabel(f"{act_type}")
                type_label.setFont(QFont("Segoe UI Variable", 10, QFont.Bold))
                type_label.setStyleSheet("color: #6366f1; background: transparent; border: none;")
                
                desc_label = QLabel(desc)
                desc_label.setFont(QFont("Segoe UI Variable", 11))
                desc_label.setStyleSheet("color: #334155; background: transparent; border: none;")
                desc_label.setWordWrap(True)
                
                time_label = QLabel(date_str)
                time_label.setFont(QFont("Segoe UI Variable", 9))
                time_label.setStyleSheet("color: #94a3b8; background: transparent; border: none;")
                
                activity_layout.addWidget(type_label)
                activity_layout.addWidget(desc_label)
                activity_layout.addWidget(time_label)
                
                self.recent_activity_layout.addWidget(activity_widget)
        
        self.recent_activity_layout.addStretch()