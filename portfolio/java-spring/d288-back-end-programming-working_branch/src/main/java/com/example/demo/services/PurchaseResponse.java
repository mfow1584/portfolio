package com.example.demo.services;

import lombok.*;

@Getter
@Setter
public class PurchaseResponse {
    private String orderTrackingNumber;
    public PurchaseResponse(String orderTrackingNumber) {
        this.orderTrackingNumber = orderTrackingNumber;
    }
}
