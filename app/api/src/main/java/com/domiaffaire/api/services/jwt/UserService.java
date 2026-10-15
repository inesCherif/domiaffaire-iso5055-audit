package com.domiaffaire.api.services.jwt;

import com.domiaffaire.api.entities.User;
import org.springframework.security.core.userdetails.UserDetailsService;

public interface UserService {
    UserDetailsService userDetailsService();
    void resetUserPassword(User user, String newPassword);
}
