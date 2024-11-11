module RCA_tb;
  reg [7:0] a, b, c;
  wire [10:0] foo;

  // Instantiate the RCA module
  RCA_spec rca (
    .a(a),
    .b(b),
    .c(c),
    .foo(foo)
  );

  initial begin
    // Test 1: Simple addition without carry
    a = 8'd1;
    b = 8'd2;
    c = 8'd3;
    #10;
    assert(foo == 11'd6) else $error("Test 1 failed: foo = %d", foo);

    // Test 2: Addition with carry handling
    a = 8'd255; // 0b11111111
    b = 8'd1;   // 0b00000001
    c = 8'd0;   // 0b00000000
    #10;
    assert(foo == 11'd256) else $error("Test 2 failed: foo = %d", foo);

    // Test 3: All inputs at max value
    a = 8'd255;
    b = 8'd255;
    c = 8'd255;
    #10;
    assert(foo == 11'd765) else $error("Test 3 failed: foo = %d", foo);

    // Test 4: Zero addition
    a = 8'd0;
    b = 8'd0;
    c = 8'd0;
    #10;
    assert(foo == 11'd0) else $error("Test 4 failed: foo = %d", foo);

    // Test 5: Random values
    a = 8'd123;
    b = 8'd45;
    c = 8'd67;
    #10;
    assert(foo == 11'd235) else $error("Test 5 failed: foo = %d", foo);
  end
endmodule
