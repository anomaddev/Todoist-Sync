#!/usr/bin/env python3
"""
Test script to demonstrate the Todoist sync functionality.
This creates sample files with TODO statements for testing.
"""

import os
import tempfile
from pathlib import Path

def create_test_files():
    """Create sample files with TODO statements for testing."""
    
    # Create a temporary directory for testing
    test_dir = Path("test_project")
    test_dir.mkdir(exist_ok=True)
    
    # Sample Swift file
    swift_content = '''import Foundation

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
'''
    
    # Sample Objective-C file
    objc_content = '''#import "SampleViewController.h"

@implementation SampleViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    // TODO: Add custom initialization
    [self setupCustomViews];
    
    /* TODO: Configure data source */
    [self configureDataSource];
}

- (void)setupCustomViews {
    // FIXME: Add proper constraints
    [self setupConstraints];
}

- (void)configureDataSource {
    // TODO: Implement data source methods
    self.dataSource = [[CustomDataSource alloc] init];
}

/* DONE: Add basic view setup */
- (void)setupBasicView {
    self.view.backgroundColor = [UIColor whiteColor];
}

@end
'''
    
    # Sample Python file
    python_content = '''#!/usr/bin/env python3
"""
Sample Python file with TODO statements.
"""

class DataProcessor:
    def __init__(self):
        # TODO: Add configuration validation
        self.config = {}
    
    def process_data(self, data):
        # TODO: Implement data processing logic
        if not data:
            return None
        
        # FIXME: Add proper error handling
        try:
            result = self._transform_data(data)
            return result
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def _transform_data(self, data):
        # TODO: Add data transformation logic
        return data.upper()
    
    # DONE: Add basic validation
    def validate_input(self, data):
        return isinstance(data, str)

# TODO: Add main function
def main():
    processor = DataProcessor()
    # TODO: Add command line argument parsing
    pass

if __name__ == "__main__":
    main()
'''
    
    # Write test files
    files = {
        "SampleViewController.swift": swift_content,
        "SampleViewController.m": objc_content,
        "data_processor.py": python_content
    }
    
    for filename, content in files.items():
        file_path = test_dir / filename
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"Created: {file_path}")
    
    print(f"\nTest project created at: {test_dir.absolute()}")
    print("You can now test the sync tool with:")
    print(f"python todoist_sync.py {test_dir} --dry-run")

if __name__ == "__main__":
    create_test_files() 