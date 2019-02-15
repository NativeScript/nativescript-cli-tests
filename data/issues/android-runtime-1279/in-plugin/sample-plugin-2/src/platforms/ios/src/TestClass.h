#import <Foundation/Foundation.h>

@interface TestClass : NSObject

- (NSString *)sayHey;
- (NSString *)sayName;
- (NSString *)sayName:(NSString *)name;
- (NSString *)say: (NSString *)name1 name: (NSString*)name2;

@end
