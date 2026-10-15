package com.domiaffaire.api.services.jwt;

import com.domiaffaire.api.entities.User;
import com.domiaffaire.api.repositories.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService{
    private final UserRepository userRepository;

    @Override
    public UserDetailsService userDetailsService() {
        return new UserDetailsService() {
            @Override
            public UserDetails loadUserByUsername(String username) {
                return userRepository.findFirstByEmail(username)
                        .map(User::new)
                        .orElseThrow(()->new UsernameNotFoundException("User not found"));
            }
        };
    }

    @Override
    public void resetUserPassword(User user, String newPassword) {
        user.setPwd(new BCryptPasswordEncoder().encode(newPassword));
        userRepository.save(user);
    }
}
