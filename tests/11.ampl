program EmployeeManagementSystem:
    EmployeeDatabase(db, employeeCount) -> int:
        array employeeNames;
        array employeeSalaries;
        let totalSalary = 0;
        
        for i in [0..employeeCount - 1]:
            output "Enter name for employee ", i + 1, ": ";
            input employeeNames[i];
            
            output "Enter salary for ", employeeNames[i], ": ";
            input employeeSalaries[i];
            
            let totalSalary = totalSalary + employeeSalaries[i];
        end;
        
        output "Total salary for all employees: ", totalSalary;
        return totalSalary;
    
    main:
        array departments;
        int numDepartments;
        let totalDepartmentSalary = 0;
        
        output "Enter the number of departments: ";
        input numDepartments;
        
        for i in [0..numDepartments - 1]:
            output "Enter name for department ", i + 1, ": ";
            input departments[i];
            
            output "Managing department: ", departments[i];
            let departmentSalary = EmployeeDatabase(departments[i], 3);
            
            let totalDepartmentSalary = totalDepartmentSalary + departmentSalary;
        end;
        
        output "Total salary for all departments: ", totalDepartmentSalary;
