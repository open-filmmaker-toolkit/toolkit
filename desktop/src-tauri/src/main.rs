// The Open Filmmaker Toolkit in its own window. The tools are the same pages as the website; bridge.js gives
// them real file access through Tauri, so saving goes back to the same file in every browser engine.
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::{WebviewUrl, WebviewWindowBuilder};

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_fs::init())
        .plugin(tauri_plugin_persisted_scope::init())
        .plugin(tauri_plugin_opener::init())
        .setup(|app| {
            WebviewWindowBuilder::new(app, "main", WebviewUrl::App("index.html".into()))
                .title("Open Filmmaker Toolkit")
                .inner_size(1280.0, 860.0)
                .min_inner_size(360.0, 480.0)
                .initialization_script(include_str!("../../bridge.js"))
                .build()?;
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("the Open Filmmaker Toolkit couldn't start");
}
