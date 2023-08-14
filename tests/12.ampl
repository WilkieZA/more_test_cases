program FibonacciCalculator:
    Fibonacci(n) -> int:
        if n <= 1:
            return n;
        else:
            return Fibonacci(n - 1) + Fibonacci(n - 2);

    main:
        let termCount = 10;
        
        for i in [0..termCount - 1]:
            let fibonacciNumber = Fibonacci(i);
            output "Fibonacci(", i, ") = ", fibonacciNumber;