import SwiftUI
import WebKit

struct ContentView: View {
    var body: some View {
        // TODO: YAYINA ALIRKEN BURAYI KENDI SUNUCU ADRESINIZ (RENDER / STREAMLIT CLOUD URL) ILE DEGISTIRIN
        // Örnek: URL(string: "https://deniz-radar.onrender.com")!
        // Lokal test için: URL(string: "http://127.0.0.1:8501")!
        // WebView(url: URL(string: "http://127.0.0.1:8501")!)
        
        let productionUrl = "https://deniz-radar.onrender.com" // KENDI DOMAININIZI YAZIN
        WebView(url: URL(string: productionUrl)!)
            .ignoresSafeArea()
    }
}

struct WebView: UIViewRepresentable {
    let url: URL
    
    func makeUIView(context: Context) -> WKWebView {
        let configuration = WKWebViewConfiguration()
        let webView = WKWebView(frame: .zero, configuration: configuration)
        webView.scrollView.bounces = false
        webView.isOpaque = false
        webView.backgroundColor = .clear
        return webView
    }
    
    func updateUIView(_ webView: WKWebView, context: Context) {
        let request = URLRequest(url: url)
        webView.load(request)
    }
}

#Preview {
    ContentView()
}
