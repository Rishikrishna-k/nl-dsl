from rest_framework import status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Chat, Message, Branch
from .serializers import MessageSerializer
from .utils_message_graph import get_heads, get_branch_from_head

class ChatGraphViewSet(viewsets.ViewSet):
    """
    ViewSet for graph-based chat operations: heads, branches, branch chain.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_chat(self, pk, user):
        return Chat.objects.get(pk=pk, owner=user)

    @action(detail=True, methods=['get'])
    def graph_heads(self, request, pk=None):
        chat = self.get_chat(pk, request.user)
        heads = get_heads(chat.message_graph)
        return Response({'heads': heads})

    @action(detail=True, methods=['get'])
    def branch_chain(self, request, pk=None):
        chat = self.get_chat(pk, request.user)
        head_id = request.query_params.get('head_id')
        if not head_id:
            return Response({'error': 'head_id query param required'}, status=status.HTTP_400_BAD_REQUEST)
        chain = get_branch_from_head(chat.message_graph, head_id)
        messages = Message.objects.filter(id__in=chain)
        msg_map = {str(m.id): m for m in messages}
        ordered_msgs = [msg_map[mid] for mid in chain if mid in msg_map]
        serializer = MessageSerializer(ordered_msgs, many=True)
        return Response({'chain': chain, 'messages': serializer.data})

    @action(detail=True, methods=['get'])
    def branches(self, request, pk=None):
        chat = self.get_chat(pk, request.user)
        branches = Branch.objects.filter(chat=chat)
        data = [
            {'branch_id': str(b.branch_id), 'head_message_id': str(b.head_message_id) if b.head_message_id else None}
            for b in branches
        ]
        return Response({'branches': data})

    @action(detail=True, methods=['get'])
    def siblings(self, request, pk=None):
        """
        Get all siblings (alternate versions) for a given message in the chat's message graph.
        Pass ?message_id=<message_id> as a query param.
        Returns all messages with the same parent as the given message, including the original.
        """
        chat = self.get_chat(pk, request.user)
        message_id = request.query_params.get('message_id')
        if not message_id:
            return Response({'error': 'message_id query param required'}, status=status.HTTP_400_BAD_REQUEST)
        graph = chat.message_graph or {}
        parent_id = graph.get(message_id, {}).get('parent')
        if parent_id is None:
            # Root messages: siblings are all root nodes
            sibling_ids = [mid for mid, node in graph.items() if node.get('parent') is None]
        else:
            sibling_ids = graph.get(parent_id, {}).get('children', [])
        messages = Message.objects.filter(id__in=sibling_ids)
        msg_map = {str(m.id): m for m in messages}
        ordered_msgs = [msg_map[mid] for mid in sibling_ids if mid in msg_map]
        serializer = MessageSerializer(ordered_msgs, many=True)
        return Response({'siblings': serializer.data}) 