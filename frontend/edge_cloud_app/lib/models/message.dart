class Message {
  final String text;
  final bool isUser;
  final List<String> sources;

  Message({
    required this.text,
    required this.isUser,
    this.sources = const [],
  });
}