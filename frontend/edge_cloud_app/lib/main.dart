import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Edge Cloud RAG',
      home: const ChatScreen(),
    );
  }
}

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController controller =
      TextEditingController();

  List<String> messages = [];

  Future<void> askQuestion() async {

    final question = controller.text;

    if (question.isEmpty) return;

    setState(() {
      messages.add("You: $question");
    });

    controller.clear();

    try {

      final response = await http.post(
        Uri.parse(
          "http://localhost:8000/ask",
        ),
        headers: {
          "Content-Type": "application/json"
        },
        body: jsonEncode({
          "question": question
        }),
      );

      if (response.statusCode == 200) {

        final data =
            jsonDecode(response.body);

        setState(() {
          messages.add(
            "Bot: ${data["answer"]}"
          );
        });

      } else {

        setState(() {
          messages.add(
            "Bot: Server Error"
          );
        });

      }

    } catch (e) {

      setState(() {
        messages.add(
          "Bot Error: $e"
        );
      });

    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Edge Cloud RAG"),
      ),
      body: Column(
        children: [

          Expanded(
            child: ListView.builder(
              itemCount: messages.length,
              itemBuilder: (context, index) {
                return ListTile(
                  title: Text(messages[index]),
                );
              },
            ),
          ),

          Padding(
            padding: const EdgeInsets.all(10),
            child: Row(
              children: [

                Expanded(
                  child: TextField(
                    controller: controller,
                    decoration:
                        const InputDecoration(
                      hintText:
                          "Ask a question...",
                    ),
                  ),
                ),

                IconButton(
                  icon: const Icon(Icons.send),
                  onPressed: askQuestion,
                ),

              ],
            ),
          ),
        ],
      ),
    );
  }
}