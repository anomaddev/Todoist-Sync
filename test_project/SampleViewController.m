#import "SampleViewController.h"

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
