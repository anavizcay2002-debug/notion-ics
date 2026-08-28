import Foundation

struct SyncStatus: Codable, Sendable {
    let status: String
    let updatedAt: Date
    let events: Int
    let intervalMinutes: Int

    var isOK: Bool { status == "ok" }
}

enum SyncStatusClient {
    static let url = URL(string: "https://anavizcay2002-debug.github.io/notion-ics/status.json")!

    static func fetch() async throws -> SyncStatus {
        let (data, response) = try await URLSession.shared.data(from: url)
        guard let http = response as? HTTPURLResponse, 200..<300 ~= http.statusCode else {
            throw URLError(.badServerResponse)
        }
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        return try decoder.decode(SyncStatus.self, from: data)
    }
}
