package main.java.com.snake.game.dtos;

public record TaskDto(Long id, String name, String description, String status, String priority, String dueDate, String assignedTo, Long userId) {
}