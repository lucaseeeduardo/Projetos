package com.agendamento;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class AgendamentoApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(AgendamentoApplication.class, args);
        System.out.println("\n====================================");
        System.out.println("Sistema de Agendamento de Serviços");
        System.out.println("API REST disponível em: http://localhost:8080/api");
        System.out.println("====================================\n");
    }
}