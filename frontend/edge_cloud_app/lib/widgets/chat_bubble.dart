import 'package:flutter/material.dart';
import '../models/message.dart';

class ChatBubble extends StatelessWidget {
  final Message message;

  const ChatBubble({
    super.key,
    required this.message,
  });

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: message.isUser
          ? Alignment.centerRight
          : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(
          horizontal: 10,
          vertical: 5,
        ),
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: message.isUser
              ? Colors.blue
              : Colors.grey.shade300,
          borderRadius:
              BorderRadius.circular(15),
        ),
        child: Column(
          crossAxisAlignment:
              CrossAxisAlignment.start,
          children: [

            Text(
              message.text,
              style: TextStyle(
                color: message.isUser
                    ? Colors.white
                    : Colors.black,
              ),
            ),

            if (!message.isUser &&
                message.sources.isNotEmpty) ...[

              const SizedBox(height: 10),

              const Text(
                "Sources",
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                ),
              ),

              const SizedBox(height: 5),

              ...message.sources.map(
                (source) => Text(
                  "• $source",
                  style: const TextStyle(
                    fontSize: 12,
                  ),
                ),
              ),

            ],
          ],
        ),
      ),
    );
  }
}