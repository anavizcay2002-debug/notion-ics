import SwiftUI

struct SyncStatusView: View {
    let status: SyncStatus?
    let error: Error?

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("Notion Calendar")
                .font(.headline)

            if let status {
                Label(status.isOK ? "Sincronizado" : "Revisar sincronización",
                      systemImage: status.isOK ? "checkmark.circle.fill" : "exclamationmark.triangle.fill")
                    .foregroundStyle(status.isOK ? .green : .orange)

                Text("Última actualización")
                    .font(.caption)
                    .foregroundStyle(.secondary)

                Text(status.updatedAt, style: .relative)
                    .font(.subheadline.weight(.semibold))

                Text("\(status.events) eventos · cada \(status.intervalMinutes) min")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            } else if error != nil {
                Label("No se puede comprobar", systemImage: "wifi.exclamationmark")
                    .foregroundStyle(.orange)
            } else {
                ProgressView("Comprobando…")
            }
        }
        .padding()
    }
}

#Preview {
    SyncStatusView(status: nil, error: nil)
}
