import Foundation

class SampleViewController {
    // TODO: Implement viewDidLoad method
    func viewDidLoad() {
        // TODO: Add navigation setup
        setupNavigation()
        
        // TODO: Configure table view
        configureTableView()
    }
    
    private func setupNavigation() {
        // FIXME: Add proper navigation title
        navigationItem.title = "Sample"
    }
    
    private func configureTableView() {
        // TODO: Set up table view delegate and data source
        tableView.delegate = self
        tableView.dataSource = self
    }
    
    // DONE: Add basic UI setup
    private func setupUI() {
        view.backgroundColor = .white
    }
}
