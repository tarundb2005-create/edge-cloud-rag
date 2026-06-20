import 'package:flutter/material.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

import 'models/message.dart';
import 'widgets/chat_bubble.dart';

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

  late WebSocketChannel channel;

  List<Message> messages = [];

  int currentBotIndex = -1;

  @override
  void initState() {
    super.initState();

    channel = WebSocketChannel.connect(
      Uri.parse(
        "ws://127.0.0.1:8000/ws",
      ),
    );

    bool receivingSources = false;
    List<String> sources = [];

    channel.stream.listen((chunk) {
      if (chunk == "[SOURCES]") {
        receivingSources = true;
        return;
      }

      if (chunk == "[END]") {
        if (currentBotIndex != -1) {
          setState(() {
            messages[currentBotIndex] = Message(
              text: messages[currentBotIndex].text,
              isUser: false,
              sources: sources,
            );
          });
        }

        receivingSources = false;
        sources = [];

        return;
      }

      if (currentBotIndex == -1) {
        return;
      }

      if (receivingSources) {
        sources.add(chunk);
      } else {
        setState(() {
          messages[currentBotIndex] = Message(
            text:
                messages[currentBotIndex].text +
                chunk,
            isUser: false,
            sources:
                messages[currentBotIndex].sources,
          );
        });
      }
    });
  }

  @override
  void dispose() {
    channel.sink.close();
    controller.dispose();
    super.dispose();
  }

  Future<void> askQuestion() async {
    final question = controller.text;

    if (question.isEmpty) return;

    setState(() {
      messages.add(
        Message(
          text: question,
          isUser: true,
        ),
      );

      messages.add(
        Message(
          text: "",
          isUser: false,
          sources: [],
        ),
      );
    });

    controller.clear();

    currentBotIndex = messages.length - 1;

    channel.sink.add(question);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          "Edge Cloud RAG",
        ),
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              itemCount: messages.length,
              itemBuilder: (context, index) {
                return ChatBubble(
                  message: messages[index],
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