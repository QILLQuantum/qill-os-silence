// src/wave.rs — THE EQUATION
pub fn step(u: &mut [[f32; 512]; 512], u_prev: &[[f32; 512]; 512], r2: f32) {
    for y in 1..511 {
        for x in 1..511 {
            let laplacian = u[y][x+1] + u[y][x-1] + u[y+1][x] + u[y-1][x]
                          + u[y+1][x+1] + u[y+1][x-1] + u[y-1][x+1] + u[y-1][x-1]
                          - 8.0 * u[y][x]; // 9-point stencil
            let next = 2.0 * u[y][x] - u_prev[y][x] + r2 * laplacian;
            framebuffer::set_pixel(x, y, (next.abs() * 255.0) as u8);
        }
    }
}