/* CaratBase — perspective-correct measurement from a photograph.
 *
 * The problem with "hold a coin next to it and compare" is that a phone is never exactly
 * square to the subject. Photograph a ring beside a bank card at any realistic angle and a
 * naive pixels-per-millimetre ratio is wrong — usually by 5-15%, and worse near the frame
 * edges, which on a 1 ct stone is a couple of hundred dollars of error.
 *
 * So instead of a ratio we solve the actual projective transform. The user marks the four
 * corners of the card; because an ISO/IEC 7810 ID-1 card is exactly 85.60 x 53.98 mm, those
 * four correspondences fully determine the homography between the photo plane and the real
 * plane. Any point marked afterwards is mapped through it and measured in true millimetres.
 *
 * This is the standard Direct Linear Transform, done in plain arithmetic — no library, no
 * model, nothing leaves the device.
 */

const CARD_W_MM = 85.60, CARD_H_MM = 53.98;

/* Solve A x = b by Gaussian elimination with partial pivoting. */
function solveLinear(A, b) {
  const n = b.length;
  const M = A.map((row, i) => [...row, b[i]]);
  for (let c = 0; c < n; c++) {
    let piv = c;
    for (let r = c + 1; r < n; r++) if (Math.abs(M[r][c]) > Math.abs(M[piv][c])) piv = r;
    if (Math.abs(M[piv][c]) < 1e-12) return null;       // degenerate: corners collinear
    [M[c], M[piv]] = [M[piv], M[c]];
    for (let r = 0; r < n; r++) {
      if (r === c) continue;
      const f = M[r][c] / M[c][c];
      for (let k = c; k <= n; k++) M[r][k] -= f * M[c][k];
    }
  }
  return M.map((row, i) => row[n] / M[i][i]);
}

/**
 * Homography mapping four image points to the card's true corners in millimetres.
 * src order must be: top-left, top-right, bottom-right, bottom-left of the card.
 */
function cardHomography(src) {
  const dst = [[0, 0], [CARD_W_MM, 0], [CARD_W_MM, CARD_H_MM], [0, CARD_H_MM]];
  const A = [], b = [];
  for (let i = 0; i < 4; i++) {
    const [x, y] = src[i], [u, v] = dst[i];
    A.push([x, y, 1, 0, 0, 0, -u * x, -u * y]); b.push(u);
    A.push([0, 0, 0, x, y, 1, -v * x, -v * y]); b.push(v);
  }
  const h = solveLinear(A, b);
  if (!h) return null;
  return [h[0], h[1], h[2], h[3], h[4], h[5], h[6], h[7], 1];
}

/* Map an image point into real-world millimetres. */
function applyH(H, p) {
  const [x, y] = p;
  const w = H[6] * x + H[7] * y + H[8];
  return [(H[0] * x + H[1] * y + H[2]) / w, (H[3] * x + H[4] * y + H[5]) / w];
}

/* True distance in millimetres between two points marked on the photo. */
function measureMm(H, p1, p2) {
  const a = applyH(H, p1), b2 = applyH(H, p2);
  return Math.hypot(b2[0] - a[0], b2[1] - a[1]);
}

/* How far from square the shot was, as a sanity signal for the user.
   The card's own diagonals should be equal; the ratio tells us how oblique the angle is. */
function tiltEstimate(src) {
  const d = (a, b) => Math.hypot(src[b][0] - src[a][0], src[b][1] - src[a][1]);
  const diag1 = d(0, 2), diag2 = d(1, 3);
  const ratio = Math.min(diag1, diag2) / Math.max(diag1, diag2);
  return { ratio, degrees: Math.round(Math.acos(Math.min(1, ratio)) * 180 / Math.PI) };
}
