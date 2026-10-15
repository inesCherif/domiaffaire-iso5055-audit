package com.domiaffaire.api.services;

import com.domiaffaire.api.dto.SignupRequest;
import com.domiaffaire.api.entities.User;
import com.domiaffaire.api.exceptions.WrongCodeAccountantException;

public interface AuthService {
    User createUser(SignupRequest signupRequest,byte[] imageBytes) throws WrongCodeAccountantException;
    boolean hasUserWithEmail(String email);
}
