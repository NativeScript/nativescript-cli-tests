#import "TestClass.h"

@implementation TestClass

- (NSString *)sayHey{
      return @"Hey!";
}
- (NSString *)sayName{
    return @"SayName no param!";
}
- (NSString *)sayName:(NSString *)name{
   return @"SayName with 1 param!";
}
- (NSString *)say: (NSString *)name1 name: (NSString*)name2 {
    return @"SayName with 2 params!";
}
@end
