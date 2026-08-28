import Foundation
import Observation

@MainActor
@Observable
final class SyncViewModel {
    var status: SyncStatus?
    var isLoading = false
    var errorMessage: String?

    func refresh() async {
        isLoading = true
        errorMessage = nil
        defer { isLoading = false }
        do {
            status = try await SyncStatusClient.fetch()
        } catch {
            errorMessage = "No se pudo consultar el estado."
        }
    }
}
