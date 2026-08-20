package com.example.demo.bootstrap;

import com.example.demo.dao.CustomerRepository;
import com.example.demo.dao.DivisionRepository;
import com.example.demo.entities.Customer;
import com.example.demo.entities.Division;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class BootStrapData implements CommandLineRunner {
    private final CustomerRepository customerRepository;
    private final DivisionRepository divisionRepository;

    public BootStrapData(CustomerRepository customerRepository, DivisionRepository divisionRepository) {
        this.customerRepository = customerRepository;
        this.divisionRepository = divisionRepository;
    }

    @Override
    public void run(String... args) throws Exception {
        // skips adding Customers to repository if it is already occupied (John Doe already in database with id 1)
        if (customerRepository.count() <= 1) {
            // sets up a Division to use when creating Customer objects
            Division div = divisionRepository.getReferenceById(3L);

            // creates a set of Customer objects using generic properties
            Customer c1 = new Customer("Zakir", "Winter", "177 Lake Drive", "92842", "5749248242");
            c1.setDivision(div);
            Customer c2 = new Customer("Tessa", "Glass", "56201 Farrell Court", "46889", "8638756756");
            c2.setDivision(div);
            Customer c3 = new Customer("Teresa", "McNeil", "3847 Tower Road", "44943", "4232276396");
            c3.setDivision(div);
            Customer c4 = new Customer("Solomon", "Barnes", "9329 The Avenue", "29456", "3734337342");
            c4.setDivision(div);
            Customer c5 = new Customer("Alisa", "Bartlett", "2943 Randall Pine", "75899", "6427592386");
            c5.setDivision(div);

            // saves the Customer objects to the repository
            customerRepository.save(c1);
            customerRepository.save(c2);
            customerRepository.save(c3);
            customerRepository.save(c4);
            customerRepository.save(c5);

            System.out.println("Customers added:");
            System.out.println(customerRepository.count());
        }
    }
}