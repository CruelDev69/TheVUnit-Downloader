import customtkinter as ctk
import os
import sys
from PIL import Image
from config import APP_VERSION, SIDEBAR_WIDTH, QUALITY_OPTIONS, PRIMARY_COLOR, PRIMARY_HOVER

def create_sidebar(parent, on_theme_toggle, on_supported_sites, on_about, on_github):
    sidebar = ctk.CTkFrame(parent, width=SIDEBAR_WIDTH, corner_radius=0)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)
    logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
    logo_frame.pack(pady=30)
    
    try:
        logo_paths = [
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "thevunit_logo.png"),
            os.path.join(os.path.dirname(sys.executable), "assets", "thevunit_logo.png"),
            os.path.join(os.getcwd(), "assets", "thevunit_logo.png")
        ]
        
        logo_loaded = False
        for logo_path in logo_paths:
            if os.path.exists(logo_path):
                logo_image = Image.open(logo_path)
                logo_image = logo_image.resize((100, 100), Image.Resampling.LANCZOS)
                logo_photo = ctk.CTkImage(light_image=logo_image, dark_image=logo_image, size=(100, 100))
                logo_label = ctk.CTkLabel(logo_frame, image=logo_photo, text="")
                logo_label.image = logo_photo
                logo_label.pack()
                logo_loaded = True
                break
        
        if not logo_loaded:
            raise Exception("Logo not found")
            
    except Exception as e:
        print(f"Logo load error: {e}")
        logo_label = ctk.CTkLabel(logo_frame, text="⬇️", font=ctk.CTkFont(size=50))
        logo_label.pack()
    
    app_name = ctk.CTkLabel(
        logo_frame,
        text="TheVUnit",
        font=ctk.CTkFont(size=24, weight="bold")
    )
    app_name.pack()
    
    version_label = ctk.CTkLabel(
        logo_frame,
        text=f"Version {APP_VERSION}",
        font=ctk.CTkFont(size=11),
        text_color=("gray50", "gray60")
    )
    version_label.pack()
    
    ctk.CTkLabel(
        sidebar, 
        text="SETTINGS", 
        font=ctk.CTkFont(size=11, weight="bold"), 
        text_color=("gray40", "gray60")
    ).pack(pady=(40, 10), padx=20, anchor="w")
    
    theme_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
    theme_frame.pack(fill="x", padx=20, pady=5)
    
    ctk.CTkLabel(
        theme_frame, 
        text="🌓 Theme", 
        font=ctk.CTkFont(size=13),
        text_color=("gray10", "gray90")
    ).pack(side="left")
    
    theme_switch = ctk.CTkSwitch(
        theme_frame, 
        text="", 
        width=40,
        command=on_theme_toggle,
        onvalue="light",
        offvalue="dark"
    )
    theme_switch.pack(side="right")
    
    sites_btn = ctk.CTkButton(
        sidebar,
        text="🌐 Supported Sites",
        fg_color="transparent",
        text_color=("gray10", "gray90"),
        hover_color=("gray70", "gray25"),
        anchor="w",
        height=35,
        command=on_supported_sites
    )
    sites_btn.pack(fill="x", padx=20, pady=5)
    
    about_btn = ctk.CTkButton(
        sidebar,
        text="ℹ️ About",
        fg_color="transparent",
        text_color=("gray10", "gray90"),
        hover_color=("gray70", "gray25"),
        anchor="w",
        height=35,
        command=on_about
    )
    about_btn.pack(fill="x", padx=20, pady=5)
    
    github_btn = ctk.CTkButton(
        sidebar,
        text="💻 GitHub",
        fg_color="transparent",
        text_color=("gray10", "gray90"),
        hover_color=("gray70", "gray25"),
        anchor="w",
        height=35,
        command=on_github
    )
    github_btn.pack(fill="x", padx=20, pady=5)
    
    return sidebar

def create_url_card(parent, on_url_change):
    url_card = ctk.CTkFrame(parent, corner_radius=10)
    url_card.pack(fill="x", pady=10)
    url_header = ctk.CTkFrame(url_card, fg_color="transparent")
    url_header.pack(fill="x", padx=20, pady=(15, 5))
    
    ctk.CTkLabel(
        url_header,
        text="🔗 Video URL",
        font=ctk.CTkFont(size=14, weight="bold")
    ).pack(side="left")
    
    platform_label = ctk.CTkLabel(
        url_header,
        text="",
        font=ctk.CTkFont(size=11),
        text_color=(PRIMARY_COLOR, PRIMARY_COLOR)
    )
    platform_label.pack(side="right")
    
    url_entry = ctk.CTkEntry(
        url_card,
        height=40,
        placeholder_text="Paste video URL from any platform here...",
        font=ctk.CTkFont(size=13)
    )
    url_entry.pack(fill="x", padx=20, pady=(5, 15))
    url_entry.bind("<KeyRelease>", on_url_change)
    
    return url_entry, platform_label

def create_options_card(parent, on_format_change):
    options_card = ctk.CTkFrame(parent, corner_radius=10)
    options_card.pack(fill="x", pady=10)
    
    ctk.CTkLabel(
        options_card,
        text="⚙️ Download Options",
        font=ctk.CTkFont(size=14, weight="bold")
    ).pack(anchor="w", padx=20, pady=(15, 10))
    
    type_container = ctk.CTkFrame(options_card, fg_color="transparent")
    type_container.pack(fill="x", padx=20, pady=5)
    
    ctk.CTkLabel(
        type_container,
        text="Type:",
        font=ctk.CTkFont(size=13),
        width=100
    ).pack(side="left")
    
    type_var = ctk.StringVar(value="Single Video")
    type_segment = ctk.CTkSegmentedButton(
        type_container,
        values=["Single Video", "Playlist"],
        variable=type_var,
        selected_color=(PRIMARY_COLOR, PRIMARY_COLOR),
        selected_hover_color=(PRIMARY_HOVER, PRIMARY_HOVER),
        unselected_color=("gray80", "gray30"),
        unselected_hover_color=("gray70", "gray35")
    )
    type_segment.pack(side="left", fill="x", expand=True)
    format_container = ctk.CTkFrame(options_card, fg_color="transparent")
    format_container.pack(fill="x", padx=20, pady=5)
    
    ctk.CTkLabel(
        format_container,
        text="Format:",
        font=ctk.CTkFont(size=13),
        width=100
    ).pack(side="left")
    
    format_var = ctk.StringVar(value="Video")
    format_segment = ctk.CTkSegmentedButton(
        format_container,
        values=["Video", "Audio Only"],
        variable=format_var,
        command=on_format_change,
        selected_color=(PRIMARY_COLOR, PRIMARY_COLOR),
        selected_hover_color=(PRIMARY_HOVER, PRIMARY_HOVER),
        unselected_color=("gray80", "gray30"),
        unselected_hover_color=("gray70", "gray35")
    )
    format_segment.pack(side="left", fill="x", expand=True)
    quality_container = ctk.CTkFrame(options_card, fg_color="transparent")
    quality_container.pack(fill="x", padx=20, pady=(5, 15))
    
    ctk.CTkLabel(
        quality_container,
        text="Quality:",
        font=ctk.CTkFont(size=13),
        width=100
    ).pack(side="left")
    
    quality_var = ctk.StringVar(value="Best")
    quality_menu = ctk.CTkOptionMenu(
        quality_container,
        values=QUALITY_OPTIONS,
        variable=quality_var,
        width=200
    )
    quality_menu.pack(side="left")
    
    return type_var, format_var, quality_var, quality_menu

def create_location_card(parent, default_path, on_browse):
    location_card = ctk.CTkFrame(parent, corner_radius=10)
    location_card.pack(fill="x", pady=10)
    
    ctk.CTkLabel(
        location_card,
        text="📁 Save Location",
        font=ctk.CTkFont(size=14, weight="bold")
    ).pack(anchor="w", padx=20, pady=(15, 5))
    
    path_container = ctk.CTkFrame(location_card, fg_color="transparent")
    path_container.pack(fill="x", padx=20, pady=(5, 15))
    path_entry = ctk.CTkEntry(
        path_container,
        height=35,
        font=ctk.CTkFont(size=12)
    )
    path_entry.insert(0, default_path)
    path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
    
    browse_btn = ctk.CTkButton(
        path_container,
        text="Browse",
        width=100,
        height=35,
        command=on_browse
    )
    browse_btn.pack(side="right")
    return path_entry

def create_progress_card(parent):
    progress_card = ctk.CTkFrame(parent, corner_radius=10)
    progress_card.pack(fill="x", pady=10)
    progress_bar = ctk.CTkProgressBar(progress_card, height=8)
    progress_bar.pack(fill="x", padx=20, pady=(15, 5))
    progress_bar.set(0)
    status_label = ctk.CTkLabel(
        progress_card,
        text="Ready to download",
        font=ctk.CTkFont(size=12),
        text_color=("gray50", "gray60")
    )
    status_label.pack(pady=(5, 15))
    
    return progress_bar, status_label