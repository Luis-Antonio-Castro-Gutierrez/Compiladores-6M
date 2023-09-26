package com.microservice.amin;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;


@SpringBootApplication
@RestController
public class AminApplication {

	@GetMapping("/WeatherForecast")
	public String getMessage() {
		return "Pinche laol estas bien qlon";
	}

	public static void main(String[] args) {
		SpringApplication.run(AminApplication.class, args);
	}

}