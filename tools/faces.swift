// Detects faces with Apple's Vision framework (macOS only).
// Usage: swift tools/faces.swift image1.jpg image2.jpg ...
// Prints JSON: {"file": [[x, y, w, h], ...]} with values 0-1 measured from the top-left of the image.
import Foundation
import Vision
import AppKit

var out: [String: [[Double]]] = [:]
for path in CommandLine.arguments.dropFirst() {
    guard let img = NSImage(contentsOfFile: path),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { continue }
    let req = VNDetectFaceRectanglesRequest()
    try? VNImageRequestHandler(cgImage: cg, options: [:]).perform([req])
    let boxes = (req.results ?? []).map { f -> [Double] in
        let b = f.boundingBox
        return [Double(b.minX), Double(1 - b.maxY), Double(b.width), Double(b.height)]
    }
    out[(path as NSString).lastPathComponent] = boxes
}
let data = try! JSONSerialization.data(withJSONObject: out, options: [.sortedKeys])
print(String(data: data, encoding: .utf8)!)
