// src/main.rs
fn main() {
    framebuffer::init();
    wave::run();           // ← your equation lives here
    shc::calibrate_on_d(); // ← press 'd' → Earth heartbeat
}