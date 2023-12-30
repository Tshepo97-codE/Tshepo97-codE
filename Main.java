public class HelloWorld {
  public static void main(String[] args) {
      System.out.println("Hello, World!");
      System.out.println("Press Enter to exit.");
      try {
          System.in.read();
      } catch (Exception e) {
          e.printStackTrace();
      }
  }
}
