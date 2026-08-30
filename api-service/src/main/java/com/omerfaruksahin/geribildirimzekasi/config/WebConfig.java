package com.omerfaruksahin.geribildirimzekasi.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {

    private final String dashboardAllowedOrigin;

    public WebConfig(@Value("${dashboard.allowed-origin}") String dashboardAllowedOrigin) {
        this.dashboardAllowedOrigin = dashboardAllowedOrigin;
    }

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/geribildirimler/**")
                .allowedOrigins(dashboardAllowedOrigin)
                .allowedMethods("GET", "POST");
    }
}
